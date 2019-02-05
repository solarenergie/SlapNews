import feedparser
import json
from urllib.request import urlopen
from urllib.error import URLError
import sqlite3
from calendar import timegm
from random import choice

class NewsDB:
	def __init__(self, feeds_filename, db_filename):
		self.db_filename = db_filename
		with open(feeds_filename) as f:
			self.feeds = json.load(f)
	def update(self):
		"""fetch new news from the feeds"""
		for source, url in self.feeds.items():
			#get already downloaded news
			done = self.conn.execute("SELECT link FROM news WHERE source=?", (source,))
			done = {each[0] for each in done}

			try:
				parsedFeed = feedparser.parse(url)

				for item in parsedFeed.entries:
					if item.link not in done:
						try:
							response = urlopen(item.link)
							page = response.read().decode("utf-8")
							unix_time = timegm(item.published_parsed)
							self.add(source, item.link, unix_time, page)
						except URLError:
							print("Failed to download {}".format(item.link))
						except Exception as e:
							print("Exception: {} at url: {}".format(str(e), item.link))
			except URLError:
				print("Failed to download {}".format(url))
	def add(self, source, link, date, content):
		"""add an article to the db
		the article is marked as unseen and unscored"""
		with self.conn:
			self.conn.execute("INSERT INTO news(source, link, date, score, page) VALUES(?, ?, ?, ?, ?)", (source, link, date, -1, content))
	def __enter__(self):
		self.conn = sqlite3.connect(self.db_filename)
		with self.conn:
			self.conn.execute("""
				CREATE TABLE IF NOT EXISTS news (
					source	TEXT	NOT NULL,
					link	TEXT	NOT NULL,
					date	INTEGER	NOT NULL,
					score	INTEGER NOT NULL,
					page	TEXT	NOT NULL
				)
			""")

		return self
	def __exit__(self, exc_type, exc_value, traceback):
		self.conn.commit()
		self.conn.close()
	def random_unscored(self):
		"""return the source and the link of a random unseen article"""
		news = list(self.conn.execute("SELECT source, link FROM news WHERE score = -1"))
		return choice(news)
	def add_score(self, source, link, score):
		with self.conn:
			self.conn.execute("UPDATE news SET score = ? WHERE source = ? AND link = ?", (score, source, link))
	def unscored(self):
		"""return a list of all unscored articles as dictionary"""
		unscored = self.conn.execute("SELECT source, link, page FROM news WHERE score = -1")
		return list(map(lambda article: {"source": article[0], "link": article[1], "page": article[2]}, unscored))
	def scored(self):
		"""return a list of all scored articles as dictionary"""
		scored = self.conn.execute("SELECT source, link, score, page FROM news WHERE score != -1")
		return list(map(lambda article: {"source": article[0], "link": article[1], "score": article[2], "page": article[3]}, scored))
	def hasNoScoredArticles(self):
		"""return true if there is no scored article in the database"""
		if len(self.scored()) == 0:
			return True
		else:
			return False

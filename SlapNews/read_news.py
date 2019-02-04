#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from SlapNews.newsdb import NewsDB
from random import shuffle
from SlapNews.ai import Pipeline1
import os
import sys
from pkg_resources import resource_filename
import shutil

classes = ["schlecht", "eher schlecht", "eher gut", "gut"]

def main():
	appdir = get_appdir()

	feeds_filename = os.path.join(appdir, "feeds.json")
	#if feeds file doesn't exist create one
	if not os.path.isfile(feeds_filename):
		shutil.copy(resource_filename(__name__, "feeds.json"), feeds_filename)

	db_filename = os.path.join(appdir, "news.db")

	Ranker = Pipeline1()

	with NewsDB(feeds_filename=feeds_filename, db_filename=db_filename) as db:
		db.update()

		if db.hasNoScoredArticles():
			rate_random(db)

		train(db, Ranker)

		while True:
			unseen = db.unscored()
			content = map(lambda x: x['page'], unseen)
			idx = Ranker.transform(content)
			for i in idx:
				print(unseen[i]["link"])

				score = ask()

				db.add_score(unseen[i]["source"], unseen[i]["link"], score)

def train(db, Ranker):
	news = db.scored()
	contents = tuple(map(lambda x: x['page'], news))
	scores = tuple(map(lambda x: x['score'], news))
	Ranker.fit(contents, scores)

def ask():
	print("Wie findest du den Artikel?")

	unordered_calsses = list(classes)
	shuffle(unordered_calsses)
	for each in unordered_calsses:
		print("\t{}".format(each))

	while True:
		answer = input().lower()
		if answer in classes:
			return classes.index(answer)
		else:
			print("Unpassende Antwort")
			continue

def rate_random(db):
	source, link = db.random_unscored()

	print(link)

	score = ask()

	db.add_score(source, link, score)

def get_appdir():
	"""get the path for application and configuration data
	if the folder does not exist it will be created"""
	if sys.platform == "win32":
		appdir = os.path.join(os.getenv('APPDATA'), "SlapNews")
	elif sys.platform == "linux":
		appdir = os.path.join(os.getenv('HOME'), ".SlapNews")
	else:
		raise "Unknown platform: {}".format(sys.platform)

	os.makedirs(appdir, exist_ok=True)

	return appdir

if __name__ == "__main__":
	main()

#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from newsdb import NewsDB
from random import shuffle
from ai import Pipeline1

classes = ["schlecht", "eher schlecht", "eher gut", "gut"]

def main():
	Ranker = Pipeline1()

	with NewsDB() as db:
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

if __name__ == "__main__":
	main()

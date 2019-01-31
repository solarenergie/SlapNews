#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from newsdb import NewsDB
from random import shuffle

classes = ["schlecht", "eher schlecht", "eher gut", "gut"]

def main():
	with NewsDB() as db:
		db.update()

		while True:
			show_random_and_ask(db)

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

def show_random_and_ask(db):
	source, link = db.random_unseen()

	print(link)

	score = ask()

	db.add_score(source, link, score)

if __name__ == "__main__":
	main()

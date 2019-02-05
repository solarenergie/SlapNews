#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import sklearn
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class SimpleRanking(sklearn.base.TransformerMixin):
	"""the articles are sorted by the propabillity of being in the most relevant class"""
	def transform(self, X):
		"""return the index of articles sorted  by relevance in descending order"""
		#convert ndarray to list
		X = X.tolist()

		#add an index to the class probability
		indexed = list(zip(X, range(len(X))))

		#sort the articles
		ranked = sorted(indexed, key=lambda x: x[0][-1], reverse=True)

		#return the index of the
		return [idx for x, idx in ranked]

class Pipeline1:
	def __init__(self, filename="Pipeline1"):
		self.clf = {
			"Preprocessing": TfidfVectorizer(),
			"Classifier": LogisticRegression(),
			"Ranking": SimpleRanking()
		}
	def fit(self, X, Y):
		X = self.clf["Preprocessing"].fit_transform(X)
		self.clf["Classifier"].fit(X, Y)
		return self
	def transform(self, X):
		X = self.clf["Preprocessing"].transform(X)
		X = self.clf["Classifier"].predict_proba(X)
		return self.clf["Ranking"].transform(X)

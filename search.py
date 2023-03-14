# Contributors
#	Victor Chhun
#	Haver  Ho

# search.py
# Search Component of the Search Engine

# Import
import pickle
import time
import linecache
import json
import nltk
import re
import shelve
import math
from collections import defaultdict
from operator import itemgetter
from functools import reduce
from nltk.stem import PorterStemmer
from engine import TD_Attributes

# File Names
indexFile = "finalResult.txt"
URLFile = "urls.txt"
wordsFile = "words.txt"
stopwordsFile = "stopwords"

indexF = open(indexFile, "r")
stopwordsF = open(stopwordsFile, "rb")

linecache.getline(indexFile, 0)
# Porter Stemmer Algorithm
ps = PorterStemmer()

# Loading in information required
stopwords = pickle.load(stopwordsF)
termShelf = shelve.open("index.shelve")
termShelf[ps.stem("of")]

# Helper Functions
# Change stop words to a set
def findStopWords(listOfWords):
	nonStopWords = list();
	for word in listOfWords:
		if word not in stopwords:
			nonStopWords.append(word)
			
	return nonStopWords

# Returns the set of unique terms of the query
def getUniqueTerms(termList):
	return list(set(termList))

# Retrieves the shelf associating with each term and append it
# to a list
# Return list of shelf's keys
# Error: Return -1
def getQueryShelf(terms):
	startTime = time.time()
	queryResult = list()
	for word in terms:
		stemWord = ps.stem(word)
		if stemWord not in termShelf:
			return -1
		# Info contains the TF and TF-IDF score  associating with the term to document
		# Info == [DF, TF-IDF Score]
		info = termShelf[stemWord]
		queryResult.append((info[0], info[1]))
	return queryResult

# Main Function
def run(query):
	query = query.lower();
	splitQ = re.split("[^a-zA-Z0-9]+", query)

	splitQ = getUniqueTerms(splitQ)
	removeStopWords = findStopWords(splitQ)
	
	# With Shelve
	queryResult = list()
	queryResult = getQueryShelf(splitQ);

	# Error Message when the query has found a word that does not exist
	# or contain misspellings
	if queryResult == -1:
		print("The query you search for either contain misspellings or does not match with any documents")
		print("Please re-enter your search query!\n")
		return -1
	
	# If there are no errors and the queryResult is non-empty
	if queryResult != -1 and len(queryResult) > 0:
	
		# Sorts the query result by their frequency
		# lowest frequency --> largest frequency
		queryResult = sorted(queryResult, key = lambda x: x[0])

		# Set initial intersection as the first query term (also the lowest frequency)
		intersection = queryResult[0][1]
		
		# Go through all terms and find the intersection.
		# Starting from the lowest set of intersection
		# to the largest set of intersection 
		for index in range(1, len(queryResult)):
			keys = intersection.keys()
			innerIntersection = dict()
			for docID in keys:

				if docID in queryResult[index][1]:
					# Keep the TF-IDF score of whichever is bigger
					if intersection[docID][1] < queryResult[index][1][docID][1]:
						innerIntersection[docID] = intersection[docID]
					else:
						innerIntersection[docID] = queryResult[index][1][docID]
			# Reset the intersection dictionary for the next iteration	
			intersection = innerIntersection
		
		# Sort the intersection dictionary by highest TF-IDF score
		intersection = dict(sorted(intersection.items(), key = lambda x: x[1][1], reverse = True))

		# Sort list tuples by highest score 
		tuples = sorted(intersection.items(), key = lambda x: x[1][1], reverse = True)

		# Get the top 5 results and
		# Retrieve their associated URL link
		TopRanks = list()
		for tup in tuples:
			if len(TopRanks) > 9:
				break;
			docID = tup[0]
			TopRanks.append( linecache.getline(URLFile, docID).strip("\n") )
			print(linecache.getline(URLFile, tup[0]).split("|")[0].strip("\n"))

		return TopRanks
if __name__ == "__main__":
	while (1):
		query = input("Enter the query: ")
		run(query)
		

# Contributors:
# 	Victor Chhun
# 	Haver  Ho

# engine.py 
# Engine component of the Search Engine
# Imports
import os
import json			# To read JSON files
import pickle		# To store particular data structures
import re			# Tokenizer
import linecache	# Retrieval of lines from a file 
import shelve		# Storage for large data structure
import time			# Time for process
import math			# To calculate TF-IDF Score
from collections import defaultdict
from nltk.stem import PorterStemmer					# Stemming
from bs4 import BeautifulSoup						# Parsing HTML/XML documents
from generateStopWords import generateStopWords		# StopWords
from copy import deepcopy

# Directory Path
directory = 'developer/DEV/'
listOfDirectories = os.listdir(directory) 	# List of folders
# Global Variables
docID = 1
indexCounter = 1
urlCounter = 0;
invertedIndex = defaultdict(list)			# In-memory inverted index
ps = PorterStemmer()						# Stemming
tokenizer = "[^a-zA-Z0-9]+"					# Tokenizer split

# Class Structure to hold key information such as
# TF-IDF Score, Term Frequency (TF), Title, Bold Words, Heading
class TD_Attributes:
	def __init__(self, score, termFreq=0, title=False, bold=False, heading=False):

		self.tf = termFreq;
		self.title = title
		self.bold = bold;
		self.heading = heading
		self.score = score
	def __repr__(self):
		return "TD_Attributes({}, {}, {}, {}, {})".format(self.score, self.tf, self.title, self.bold, self.heading)

# Return the set of Bold words found in a document
def getSetOfBold(soup):
	tagSet = set();
	for phrase in soup.find_all(["b", "strong"]):
		if phrase.string:
			for token in re.split(tokenizer, phrase.string):
				token = ps.stem(token)
				if len(token) > 0:
					tagSet.add(token)
	return tagSet

# Return the set of Heading words found in a document
def getSetOfHeading(soup):
	headingSet = set();
	for phrase in soup.find_all(["h1","h2","h3"]):
		if phrase.string:
			for token in re.split(tokenizer, phrase.string):
				token = ps.stem(token);
				if len(token) > 0:
					headingSet.add(token);
	return headingSet;

# Return the set of Title words found in a document
def getSetOfTitle(soup):
	titleSet = set()
	if soup.title and soup.title.string:
		for token in re.split(tokenizer, soup.title.string):
			token = ps.stem(token)
			if len(token) > 0:
				titleSet.add(token)
	return titleSet


# Retrieve a line from a file
# using linecache
# Return the retrieved line
def getLine(fileName, lineNo):
	line = linecache.getline(fileName, lineNo)
	line = line.split("|")
	if line != [""]:
		line[1] = int(line[1])
		line[2] = line[2].rstrip() + ","
		line[2] = eval(line[2])
	return line

# Write to a partial index file
# which will be merged later
def writeToFile(indexFileName):
	if indexFileName == 1:
		indexFileName = "partial1.txt"
	elif indexFileName == 2:
		indexFileName = "partial2.txt"
	else:
		indexFileName = "partial3.txt"
	inFile = open(indexFileName, "w")
	for item in sorted(invertedIndex):

		strDict = str(invertedIndex[item][1])
		line = item + "|" + str(invertedIndex[item][0]) + "|" + strDict + "\n"
		inFile.write(line)
	inFile.close()

# Translate a line from a file that is stored in the order of
# Term | DF | {docID: class }
def getInfo(line):
	line = line.split("|")
	saved =  ""
	if line != ['']:	
		line[1] = int(line[1])
		line[2] = line[2].rstrip()
		line[2] = eval(line[2])
	return line

# Writes one line to a file with the given information
def writeLineToFile(word, count, dictionary, file):
	file.write(str(word) + "|" + str(count) + "|" + str(dictionary) + "\n")

# Merges two files at a time and writes to a 
# result file
def mergeTwo(file1, file2, resultFile):
	# Open all three files 
	partialA = open(file1, "r")
	partialB = open(file2, "r")
	resultF = open(resultFile, "w")
	lineA = partialA.readline()
	lineB = partialB.readline()

	# While there both files still contain lines to read
	while (lineA and lineB):
		mergeDict = dict()

		# Both returns a list.
		# They are structured as
		# [Term, DF, {docID: class} ]
		infoA = getInfo(lineA)
		infoB = getInfo(lineB)
	
		# If both terms are equal on both files,
		# merge the line and update their information
		if (infoA[0] == infoB[0] and infoA != ['']):
			dictA = infoA[2]
			dictB = infoB[2]
			count = infoA[1]
			tempA = deepcopy(dictA)
			for docID in dictA:
				# Update information if it appears in both dictionary
				if docID in dictB:
					tempA[docID].tf += tempB[docID].tf
					tempA[docID].title = tempA[docID].title or dictB[docID].title
					tempA[docID].bold = tempA[docID].bold or dictB[docID].bold
					tempA[docID].heading = tempA[docID].heading or dictB[docID].heading
				# Else, add information to dictionary
				else:
					for docBID in dictB:
						tempA[docBID] = dictB[docBID]
					count += 1
			# Write the updated information into the result file
			writeLineToFile(infoA[0], count, tempA, resultF)
			
			# Update the two file pointers
			lineA = partialA.readline()
			lineB = partialB.readline()
		# If termA is "less" than termB,
		# write lineA information into result file
		# as it will appear eariler in the document
		elif (infoA[0] < infoB[0]):
			writeLineToFile(infoA[0], infoA[1], infoA[2], resultF)
			lineA = partialA.readline()
		# Else, termB is "less" than termA,
		# write lineB information into the result file
		# as it will appear eariler in the document
		else:
			writeLineToFile(infoB[0], infoB[1], infoB[2], resultF)
			lineB = partialB.readline()
	
	# While there are still lines need to be check in lineA.
	# In other words, fileB ran out of lines but fileA still contain lines.
	# Everything found in fileA are guaranteed to come later than anything in fileB
	while (lineA):
		infoA = getInfo(lineA)
		writeLineToFile(infoA[0], infoA[1], infoA[2], resultF)
		lineA = partialA.readline()

	# While there are still ines need to be check in lineB.
	# In other words, fileA ran out of lines but fileB still contain lines.
	# Everything found in fileB are guaranteed to come later than anything in fileA
	while (lineB):
		infoB = getInfo(lineB)
		writeLineToFile(infoB[0], infoB[1], infoB[2], resultF)
		lineB = partialB.readline()
	
	# Close all three files
	partialA.close()
	partialB.close()
	resultF.close()

# Transforms the given list into a dictionary format to evaluate
# during the query processing
def listToFileFormat(targetList):
	strDict = "{" + ', '.join(["{}: {}".format(key, value) for key, value in targetList[2].items()]) + "}"
	return targetList[0] +  "|" + str(targetList[1]) + "|" + strDict + "\n"

# Calculates the TF --> Term Frequency --> 1 + log ( Raw count / # of Words)
#				# of words come from file
#				Raw Count come from dictionary docID: freq
def calculateTF(Raw, Total):
	tf = Raw
	weight = 1 + math.log(tf, 10)
	return weight if tf > 0  else 0;

# Calculates the IDF --> Inverse Document Frequency --> log ( N / docFreq )
#					where N is the total number of documents and 
#					docFreq is the number of documents word appear in
def calculateIDF(N, docFreq):
	weight = math.log(N / docFreq, 10)
	return weight

# Calculates the TF-IDF score
def calculateScore(filename, N, resultFile):
	file = open(filename, "r")
	resultF = open(resultFile, "w")
	line = file.readline()
	while (line):
		line = line.split("|")
		word = line[0];
		docFreq = int(line[1])
		# Dictionary --> {docID: class}
		dictionary = eval(line[2].rstrip())
		newRank = dict()
		for docID in dictionary.keys():
			Total = int(linecache.getline("words.txt", docID))
			Raw = int(dictionary[docID].tf)
			bold = 0
			heading = 0
			title = 0
			if dictionary[docID].bold:
				bold = 0.02
			if dictionary[docID].heading:
				heading = 0.10
			if dictionary[docID].title:
				title = 0.25
			score = calculateTF(Raw, Total) * calculateIDF(N, docFreq) * (1 + bold  + heading + title)
			# Rounding score to 5 decimal places
			dictionary[docID].score = round(score, 5) 
		sortedDict = dict(sorted(dictionary.items(), key = lambda x: x[1].score, reverse = True))
		resultF.write(word + "|" + str(docFreq) + "|" + str(sortedDict)  + "\n")
		line = file.readline()
	file.close()
	resultF.close()

# Checks if we have seen the url before
# Return -1 if it is a URL we have seen before
# Return 1 if it is a new URL
def checkURL(url):
	global urlCounter
	openURLs = open("seenURL.txt", "r")
	# Defrag the URL
	url = url.split("#")
	for line in openURLs.readlines():
		if url[0] == line.strip("\n"):
			urlCounter += 1
			openURLs.close()
			return -1
	openURLs.close()
	openURLs = open("seenURL.txt", "a")
	openURLs.write(url[0] + "\n")
	openURLs.close()
	return 1


# Creates the shelf object to store the inverted index matrix.
# This will be the main object the "search" part of the engine will use
def createShelfFile(mergeDoc):
	with shelve.open("index.shelve") as termShelf:
		with open(mergeDoc, "r") as merge:
			line = merge.readline()
			
			while (line):
				if (len(line) > 0):
					line = line.split("|")
					line[1] = int(line[1])
					line[2] = line[2].rstrip()
					# {docID: class}
					line[2] = eval(line[2])

					# Convert class into a list of [TF, TF-IDF score]
					infoDictionary = dict()
					for docID in line[2]:
						infoDictionary[docID] = [ line[2][docID].tf, line[2][docID].score ]
					line[2] = infoDictionary

					termShelf[ line[0] ] = line[1: ]
					line = merge.readline()

# Main Program
def run():
	global docID
	global indexCounter
	global urlCounter
	words = open("words.txt", "w")
	seenUrl = open("seenURL.txt", "w")
	urls = open("urls.txt", "w", encoding = "utf-8")
	counter = 1
# ------------------------------------------------------------------------------ #
	for directoryEntry in listOfDirectories:
		for filename in os.scandir(directory + directoryEntry):
			if filename.is_file():
				docTime = time.time()
				# Opens the json file for reading
				# JSON file contains: 'url', 'content', 'encoding'
				file = open(filename)
				data = json.load(file)
				soup = BeautifulSoup(data['content'], 'html.parser')
				tokens = re.split(tokenizer, soup.get_text())
				link = data['url']

				# Checks if the URL is a duplicated page
				# duplicated page is when the url is the same as another 
				# webpage we have already seen
				if checkURL(link) != -1:
					words.write(str(len(tokens)) + "\n")
					# Counter for word position in the file
					wordPos = 0;
					# Retrieve the set of all words that are considered "important"
					# Important words are those in titles, headings (h1, h2, h3), and
					# bold words ('b', 'strong')
					titleSet = getSetOfTitle(soup)
					headingSet = getSetOfHeading(soup)
					tagSet = getSetOfBold(soup)
					# Loop through all tokens found in the document
					# and count their frequency
					# to construct the inverted index
					for word in tokens:
						# Stemming the word
						stem = ps.stem(word.lower())

						if (len(stem) > 0):
							# Constructing the first instance of
							# key-value pair in the inverted index
							if stem not in invertedIndex:
								# invertedIndex == { stem: [DF, {docID: class } ] }
								invertedIndex[stem];
								# DF
								invertedIndex[stem].append(1)
								# {docID: class}
								invertedIndex[stem].append({docID: TD_Attributes(0)})
								invertedIndex[stem][1][docID].tf += 1		
							else:
							# Else, we want to increment the counters
								if (docID not in invertedIndex[stem][1].keys()):
									invertedIndex[stem][0] += 1
									invertedIndex[stem][1][docID] = TD_Attributes(0)
								invertedIndex[stem][1][docID].tf += 1
							# Checks if stem word is an important word
							if stem in titleSet:
								invertedIndex[stem][1][docID].title = True
							if stem in tagSet:
								invertedIndex[stem][1][docID].bold = True
							if stem in headingSet:
								invertedIndex[stem][1][docID].heading = True;
						# Write to a partial index at a certain counter
						if counter >= 20000:
							writeToFile(indexCounter)
							indexCounter += 1;
							invertedIndex.clear()
							counter = 0
					# Write url to a file for the query processing to use
					urls.write(data['url'] + '\n')
					# Increment both docID and counter
					docID += 1
					counter += 1
# -------------------------------------------------------------------------------------- #

	urls.close()
	words.close()
	# If there are any left over files in the inverted index
	# Write to a partial file for merging later
	if (counter > 0):
		writeToFile(indexCounter)
		indexCounter += 1
		counter  = 0
	mergeTwo("partial1.txt", "partial2.txt", "merge1.txt")
	mergeTwo("partial3.txt", "merge1.txt", "mastermerge.txt")	
	calculateScore("mastermerge.txt", docID, "finalResult.txt")
	createShelfFile("finalResult.txt")
	setOfStopWords = generateStopWords()
	stopwords = open("stopwords", "wb")
	pickle.dump(setOfStopWords, stopwords)
	stopwords.close()
	
if __name__ == "__main__":
	run()


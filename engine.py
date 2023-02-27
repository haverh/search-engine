# engine.py
# The engine of the Search Engine
# MS1

import os
import json									# Parsing JSON files
from nltk.tokenize import word_tokenize		# For tokenizing
from nltk.stem import PorterStemmer			# For Stemming
from collections import defaultdict
import pickle								# Storing defaultdict data structure
import sys
import re									# Splitting/Tokenizing
from bs4 import BeautifulSoup				# Parsing JSON 'content'

# Path to the DEV folder containing all folders w/ their json files
# directory = 'analyst/ANALYST/'
directory = 'developer/DEV/'
# file = 'analystIndexer2'
file = 'devTest'
fileOpen = open(file, "wb")
# Global DocID
docID = 1

# Default Dictionary {word : { docID } }
# Set to prevent duplicates docID
invertedIndex = defaultdict(list)

# List of all directory folders
listOfDirectories = os.listdir(directory)

# Porter Stemming Algorithm
ps = PorterStemmer()

urls = open('urls.txt', 'w')
# Iterate through the listOfDirectories
for directoryEntry in listOfDirectories:
# Scan for filename and checks if they are a file we can open
	# e.g. json files
	for filename in os.scandir(directory + directoryEntry):
		if filename.is_file():
			# Parse the json file
			file = open(filename)
			data = json.load(file)
			# Load the json 'content' and parse with BeautifulSoup
			# json 'content' is in HTML format
			soup = BeautifulSoup(data['content'], 'html.parser')
			# Split at non-alphanumeric characters
			tokens = re.split("[^a-zA-Z0-9]+", soup.get_text())
			# Lowercase the words
			for word in tokens:
				index = invertedIndex[ps.stem(word)]
				if len(index) < 1:
					index.append(1)
					index.append(defaultdict(int))
					index[1][docID] += 1
				else:
					if (docID not in index[1].keys()):
						index[0] = index[0] + 1
						index[1][docID] += 1
					else:
						index[1][docID] += 1
			urls.write(data['url']+'\n')
			# Increment docID for the next document
			docID += 1

urls.close()

# Dump the dictionary into a file
# pickle.dump(invertedIndex, fileOpen)
# fileOpen.close()

lineNo = 0
offsetDict = dict()

indexFile = open("id.txt", "a+")
offsetFile = open("offset.bin","wb")
# indexFile.write(str(len(invertedIndex)) + "\n")
lastKey = ''
key = '';
for item in sorted(invertedIndex):
	line = item + "|" + str(invertedIndex[item][0]) + "|" + ','.join(map(str, invertedIndex[item][1].items())) + "\n"
	if len(item) > 0:
		lineNo += 1
		firstChar = item[0]
		if (firstChar != key):
			lastKey = key
			key = firstChar
			offsetDict[key] = [lineNo]
			if (lastKey != ''):
				offsetDict[lastKey].append(lineNo-1)
		indexFile.write(line)
offsetDict[key].append(lineNo)
'''
for key in offsetDict:
	print("KEY: " + key)
	if key  != "z":
		offsetDict[key].append(offsetDict[chr(ord(key)+1)][0]-1)
'''
indexFile.close()
pickle.dump(offsetDict,offsetFile)
offsetFile.close()



# For reading the file and getting size of pickle file
"""
fileOpen = open(file, "rb")
data = pickle.load(fileOpen);
#print(data)
print(sys.getsizeof(fileOpen))
print(sys.getsizeof(data) / 10000)
print(len(data.keys()))
"""

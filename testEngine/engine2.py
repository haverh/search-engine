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
# Global DocID
docID = 1
tokAmount = 0
indCounter = 1

lineNo = 0
offsetDict = dict()
lastKey = ''
key = ''
offsetFile = open("offset2.bin", "wb")

# Default Dictionary {word : { docID } }
# Set to prevent duplicates docID
invertedIndex = defaultdict(list)

# List of all directory folders
listOfDirectories = os.listdir(directory)

# Porter Stemming Algorithm
ps = PorterStemmer()

urls = open('urls2.txt', 'w')
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
            soup = BeautifulSoup(
                data['content'], 'html.parser', from_encoding=data['encoding'])
            # Split at non-alphanumeric characters
            tokens = re.split("[^a-zA-Z0-9]+", soup.get_text())
            # Lowercase the words
            for word in tokens:
                if ps.stem(word) not in invertedIndex:
                    invertedIndex[ps.stem(word)]
                    invertedIndex[ps.stem(word)].append([1, 0])
                    invertedIndex[ps.stem(word)].append(defaultdict(int))
                    invertedIndex[ps.stem(word)][1][docID] += 1
                    tokAmount += 1
                else:
                    if (docID not in invertedIndex[ps.stem(word)][1].keys()):
                        invertedIndex[ps.stem(word)][0][0] += 1
                    invertedIndex[ps.stem(word)][1][docID] += 1

            if (docID % 15000 == 0):
                print(tokAmount)
                inFile = open("index"+str(indCounter)+".txt", "a+")
                for item in sorted(invertedIndex):
                    line = item + "|" + str(invertedIndex[item][0]) + "|" + \
                        ','.join(
                            map(str, invertedIndex[item][1].items())) + "\n"
                    if len(item) > 0:
                        lineNo += 1
                        firstChar = item[0]
                        if (firstChar != key):
                            lastKey = key
                            key = firstChar
                            offsetDict[key] = [lineNo]
                            if (lastKey != ''):
                                offsetDict[lastKey].append(lineNo-1)
                        inFile.write(line)

                offsetDict[key].append(lineNo)
                indCounter += 1
                invertedIndex.clear()

            urls.write(data['url']+'\n')
            # Increment docID for the next document
            docID += 1

urls.close()

inFile = open("index"+str(indCounter)+".txt", "a+")
for item in sorted(invertedIndex):
    line = item + "|" + str(invertedIndex[item][0]) + "|" + \
        ','.join(
            map(str, invertedIndex[item][1].items())) + "\n"
    if len(item) > 0:
        lineNo += 1
        firstChar = item[0]
        if (firstChar != key):
            lastKey = key
            key = firstChar
            offsetDict[key] = [lineNo]
            if (lastKey != ''):
                offsetDict[lastKey].append(lineNo-1)
        inFile.write(line)

offsetDict[key].append(lineNo)

inFile.close()
pickle.dump(offsetDict, offsetFile)
offsetFile.close()

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
import linecache

# Path to the DEV folder containing all folders w/ their json files
# directory = 'analyst/ANALYST/'
directory = 'developer/DEV/'
# Global DocID
docID = 1
tokAmount = 0
indCounter = 1

lineNo = 1
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


def getLine(fileName,lineNo):
    line = linecache.getline(fileName, lineNo)
    line = line.split('|')
    if line != ['']:
        line[1] = int(line[1])
        line[2] = line[2].rstrip() + ','
        line[2] = dict(ast.literal_eval(line[2]))
    return line
    
def listToFileFormat(targetList):
    return targetList[0] + "|" + str(targetList[1]) + "|" + \
            ','.join(map(str, targetList[2].items())) + "\n"

def mergeTwo(file1Pointer, file2Pointer, file1Amount, file2Amount, mergedFile):

    while (file1Pointer <= int(file1Amount) or file2Pointer <= int(file2Amount) ):
        line1 = getLine('file1.txt', file1Pointer)
        line2 = getLine('file2.txt', file2Pointer)
        
        if ( line1[0] < line2[0] or line2[0] == '' ):
            # line1 into newMergedFile
            mergedFile.write(listToFileFormat(line1))
            file1Pointer += 1
            
        elif ( line1[0] > line2[0] or line1[0] == '' ):
            # line2 into newMergedFile
            mergedFile.write(listToFileFormat(line2))
            file2Pointer += 1
            
        else:
            # print(line1[0])
            # create dict with line1[0] as key of a LIST
            word = line1[0]
            tempDict = defaultdict(list)
            tempDict[word]
            # dict[0] = 0
            tempDict[word].append(0)
            # dict[1] = dict with docID as key
            tempDict[word].append(defaultdict(int))
            # loop through each line#[1] and add
            # if docID exists add frequency
            for doc in line1[2]:
                if (doc not in tempDict[word][1]):
                    tempDict[word][1][doc] = line1[2][doc]
                else:
                    tempDict[word][1][doc] += line1[2][doc]
                    
            for doc2 in line2[2]:
                if (doc2 not in tempDict[word][1]):
                    tempDict[word][1][doc2] = line2[2][doc2]
                else:
                    tempDict[word][1][doc2] += line2[2][doc2]
                    
            line = word + "|" + str(tempDict[word][0]) + "|" + \
                ','.join(map(str, tempDict[word][1].items())) + "\n"
                
            mergedFile.write(line)
                
            file1Pointer += 1
            file2Pointer += 1


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
            # print(filename)
            soup = BeautifulSoup(
                data['content'], 'html.parser')
            soup.prettify(data['encoding'])
            # Split at non-alphanumeric characters
            tokens = re.split("[^a-zA-Z0-9]+", soup.get_text())
            # Lowercase the words
            for word in tokens:
                stemmedWord = ps.stem(word)
                if ( len(stemmedWord) > 0 ):
                    if stemmedWord not in invertedIndex:
                        invertedIndex[stemmedWord]
                        invertedIndex[stemmedWord].append([1, 0])
                        invertedIndex[stemmedWord].append(defaultdict(int))
                        invertedIndex[stemmedWord][1][docID] += 1
                        tokAmount += 1
                    else:
                        if (docID not in invertedIndex[stemmedWord][1].keys()):
                            invertedIndex[stemmedWord][0][0] += 1
                        invertedIndex[stemmedWord][1][docID] += 1

            if (docID % 15000 == 0):
                print(tokAmount)
                inFile = open("index"+str(indCounter)+".txt", "a+")
                inFile.write(str(len(invertedIndex.keys())))
                for item in sorted(invertedIndex):
                    line = item + "|" + str(invertedIndex[item][0]) + "|" + \
                        ','.join(
                            map(str, invertedIndex[item][1].items())) + "\n"
                    firstChar = item[0]
                    if (firstChar != key):
                        lastKey = key
                        key = firstChar
                        offsetDict[key] = [lineNo]
                        if (lastKey != ''):
                            offsetDict[lastKey].append(lineNo-1)
                    lineNo += 1
                    inFile.write(line)

                offsetDict[key].append(lineNo)
                indCounter += 1
                invertedIndex.clear()

            urls.write(data['url']+'\n')
            # Increment docID for the next document
            docID += 1

urls.close()

inFile = open("index"+str(indCounter)+".txt", "a+")
inFile.write(str(len(invertedIndex.keys())))
for item in sorted(invertedIndex):
    line = item + "|" + str(invertedIndex[item][0]) + "|" + \
        ','.join(
            map(str, invertedIndex[item][1].items())) + "\n"
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

submerge1 = open('submerge1.txt', 'a+')

file1Pointer = 2
file2Pointer = 2
file1Amount = int(linecache.getline('index1.txt',1)+1)
file2Amount = int(linecache.getline('index2.txt',1)+1)

mergeTwo(file1Pointer, file2Pointer, file1Amount, file2Amount, submerge1)

submerge2 = open('submerge2.txt', 'a+')

file1Pointer = 2
file2Pointer = 2
file1Amount = int(linecache.getline('index3.txt',1)+1)
file2Amount = int(linecache.getline('index4.txt',1)+1)

mergeTwo(file1Pointer, file2Pointer, file1Amount, file2Amount, submerge2)

mastermerge = open('mastermerge.txt', 'a+')

file1Pointer = 2
file2Pointer = 2
file1Amount = int(linecache.getline('submerge1.txt',1)+1)
file2Amount = int(linecache.getline('submerge2.txt',1)+1)

mergeTwo(file1Pointer, file2Pointer, file1Amount, file2Amount, mastermerge)



pickle.dump(offsetDict, offsetFile)
offsetFile.close()
submerge1.close()
submerge2.close()
mastermerge.close()

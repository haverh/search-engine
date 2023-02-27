# search.py
# Search Component of the Search Engine
# MS2
# import engine.py
# import pickle
# invertedIndexFileName = "indexer.txt"

# # User Input
# print("Using the search component of the Search Engine!")
# query = input("Enter the query you want to find: ")
# query = query.lower()
# # Split the query into individual words
# # e.g. cristina lopes ==> ["cristina", "lopes"]
# splitQuery = query.split()


# # Retriving inverted index from file stored in disk

# invertedIndexFile = open(invertedIndexFileName, "r")
# invertedIndex = pickle.load(invertedIndexFile)
# invertedIndexFile.close()


# # Boolean Query

# # Set the initial "intersection" as the first word in the query
# intersectionQuery = invertedIndex[splitQuery[0]]
# splitQuery.pop(0)
# for word in splitQuery:
#     intersectionQuery.intersection(word)
# listt = list(intersectionQuery)

# print(intersectionQuery)
# print()
# print(listt[0:5])
import ast
import linecache
from nltk.stem import PorterStemmer
import pickle
import time
from operator import itemgetter
from functools import reduce
# extracting the 3th line
# line 3 == 4
# line _ == firstline
ps = PorterStemmer()
docID = 'id.txt'
indexer = 'offset.bin'
urls = 'urls.txt'


def recache(lineNo, targetLen):
    # start3 = time.time()
    # linecache.clearcache()
    line = linecache.getline(docID, lineNo)
    # print(line[0:30])
    # print("RECACHE -> " + str(time.time() - start3))
    return line[0:30].split('|')[0]


'''
line[1] = int(line[1])
line[2] = line[2].strip() + ","
line[2] = dict(ast.literal_eval(line[2]))
#line[2] = docIDs
return line
'''


def getLine(lineNo):
    # linecache.clearcache()
    start2 = time.time()
    line = linecache.getline(docID, lineNo)
    line = line.split('|')
    line[1] = int(line[1])
    line[2] = line[2].rstrip() + ','
    line[2] = dict(ast.literal_eval(line[2]))
    print("GETLINE -> " + str(time.time()-start2))
    return line


def getUrl(docNo):
    line = linecache.getline(urls, docNo)
    return line.rstrip()


def search(low, high, piv, tar):
    while (low <= high):
        piv = int((high-low)/2) + low
        line = recache(piv, len(tar))

        if (line == tar):
            # print(piv)
            return getLine(piv)
        '''
    	if (low == high):
        	line = recache(docID,low)
        	if (line < tar): return [tar,0,dict()];
        	if (line > tar): return [tar,0,dict()];
		'''

        if (line > tar):
            high = piv-1
            # return search(low,high,piv,tar);
        else:
            low = piv+1
            # return search(low,high,piv,tar);
    return [tar, 0, dict()]


# line = recache(docID,1)
'''
low = 2
high = int(line[0]) + 1
piv = int((high-low) / 2)
'''
indexFile = open(indexer, 'rb')
offset = pickle.load(indexFile)
# print(offset)

'''
while (1):
    print("Using the search component of the Search Engine!")
    query = input("Enter the query you want to find: ")
    starttime = time.time()
    query = query.lower()
    splitQuery = query.split()

    # intersectedID = search(low, high, piv, ps.stem(splitQuery[0]))[2]

    someList = []
    for token in splitQuery:
        firstChar = token[0]
        low = offset[firstChar][0]
        high = offset[firstChar][1]
        piv = low + int((high-low)/2)
        intersectedID = search(low, high, piv, ps.stem(token))
        someList.append(intersectedID)
        print(token + " --> " + str(intersectedID[1]))

    start4 = time.time()
    someList = sorted(someList, key=itemgetter(1))

    someList = list(map(lambda x: x[2], someList))
    sect = list(reduce(lambda x, y: x & y.keys(), someList))
    for k, v in enumerate(sect):
        freq = 0
        for dic in someList:
            freq += dic[v]
        sect[k] = (freq, v)

    sect.sort(reverse=True)
    print("Processing Set -> " + str(time.time() - start4))
    for i in range(0, 5):
        sect[i] = getUrl(sect[i][1])
    print(sect[0:5])
    print(time.time() - starttime)
    '''


def searchFor(queryString):
    starttime = time.time()
    query = queryString.lower()
    splitQuery = query.split()

    # intersectedID = search(low, high, piv, ps.stem(splitQuery[0]))[2]

    someList = []
    for token in splitQuery:
        firstChar = token[0]
        low = offset[firstChar][0]
        high = offset[firstChar][1]
        piv = low + int((high-low)/2)
        intersectedID = search(low, high, piv, ps.stem(token))
        someList.append(intersectedID)
        # print(token + " --> " + str(intersectedID[1]))

    start4 = time.time()
    someList = sorted(someList, key=itemgetter(1))

    someList = list(map(lambda x: x[2], someList))
    sect = list(reduce(lambda x, y: x & y.keys(), someList))
    for k, v in enumerate(sect):
        freq = 0
        for dic in someList:
            freq += dic[v]
        sect[k] = (freq, v)

    sect.sort(reverse=True)
    # print("Processing Set -> " + str(time.time() - start4))
    for i in range(0, 5):
        sect[i] = getUrl(sect[i][1])

    return sect[0:5]
    # print(sect[0:5])
    # print(time.time() - starttime)


import ast
import linecache
from nltk.stem import PorterStemmer
import pickle
import time
from operator import itemgetter
from functools import reduce
from flask import Flask, render_template, request

ps = PorterStemmer()
docID = 'id.txt'
indexer = 'offset.bin'
urls = 'urls.txt'


def recache(lineNo, targetLen):
    line = linecache.getline(docID, lineNo)
    return line[0:30].split('|')[0]


def getLine(lineNo):
    line = linecache.getline(docID, lineNo)
    line = line.split('|')
    line[1] = int(line[1])
    line[2] = line[2].rstrip() + ','
    line[2] = dict(ast.literal_eval(line[2]))
    return line


def getUrl(docNo):
    line = linecache.getline(urls, docNo)
    return line.rstrip()


def search(low, high, piv, tar):
    while (low <= high):
        piv = int((high-low)/2) + low
        line = recache(piv, len(tar))

        if (line == tar):
            return getLine(piv)

        if (line > tar):
            high = piv-1
            # return search(low,high,piv,tar);
        else:
            low = piv+1
            # return search(low,high,piv,tar);
    return [tar, 0, dict()]


indexFile = open(indexer, 'rb')
offset = pickle.load(indexFile)

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

linecache.getline(docID, 0)


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

    print(time.time() - starttime)
    return sect[0:5]
    # print(sect[0:5])
    # print(time.time() - starttime)


app = Flask(__name__, template_folder="templates", static_folder="statics")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def homePOST():
    text = request.form["srch"]
    print(text)
    return searchFor(text)


@app.route("/search")
def searched():
    return render_template("searched.html")


@app.route("/search", methods=["POST"])
def searchedPOST():
    text = request.form["srch"]
    print(text)
    return searchFor(text)


if __name__ == "__main__":
    linecache.getline("id.txt", 0)
    app.run(debug=True)

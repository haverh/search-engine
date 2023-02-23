# search.py
# Search Component of the Search Engine
# MS2
# import engine.py
import pickle
invertedIndexFileName = "indexer.txt"

# User Input
print("Using the search component of the Search Engine!")
query = input("Enter the query you want to find: ")
query = query.lower()
# Split the query into individual words
# e.g. cristina lopes ==> ["cristina", "lopes"]
splitQuery = query.split()


# Retriving inverted index from file stored in disk

invertedIndexFile = open(invertedIndexFileName, "r")
invertedIndex = pickle.load(invertedIndexFile)
invertedIndexFile.close()


# Boolean Query

# Set the initial "intersection" as the first word in the query
intersectionQuery = invertedIndex[splitQuery[0]]
splitQuery.pop(0)
for word in splitQuery:
    intersectionQuery.intersection(word)
listt = list(intersectionQuery)

print(intersectionQuery)
print()
print(listt[0:5])

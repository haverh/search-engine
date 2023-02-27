import pickle
from sys import getsizeof

index = open('dev.bin', 'rb')
data = pickle.load(index)


print("Number of Indexed Documents --> " + str(55394))
print("Number of Unique Words --> " + str(len(data)))
print("Total Size --> " + str(getsizeof(data)/1000) + " KB")

import csv
import itertools
import time

with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))

num_of_cities = 6

indeces = [i for i in range (1, num_of_cities)]
dist = 0.0
road = [0, 0];
#start tid
start = time.time()

#for hver permutasjon m
for m in itertools.permutations(indeces):
    #start til by 1.
    temp_dist = 0.0
    #regn distanse gjennom alle byene [fra][til]
    #i = fra
    m = (0,) + m + (0,)
    for i in range (0, len(m)-1):
        temp_dist += float(data[m[i]+1][m[i+1]])
    if temp_dist < dist or dist == 0:
        dist = temp_dist
        road = m

#-------------------
#slutt tid
end = time.time()

#print
output = data[0][road[0]]
for i in range (1, len(road)):
    output += " -> " + data[0][road[i]]
print(output)
print(dist)
print("time elapsed: " + str(end - start))

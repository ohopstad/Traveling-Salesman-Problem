import csv
import itertools
import time
import random
with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))

num_of_cities = 24
num_of_retries = 15
bad_cities = num_of_cities/2

def move(road, index):
    # swaps road[index] and road[index+1]
    road[index:index+2] = reversed(road[index:index+2])
    return road

def distance(a_road):
    # calculates distance traveled in given path.
    dist = float(data[1][a_road[0]])
    for city in range(0, len(a_road)-1):
        dist += float(data[a_road[city]+1][a_road[city+1]])
    dist += float(data[a_road[-1]+1][0])
    return dist


# start tid
start = time.time()
# -------------
# always start in [0][0]'Barcelona'
indeces = [i for i in range (1, num_of_cities)]
ans_road = indeces
ans_dist = distance(ans_road)
road = ans_road
for _ in range (0, num_of_retries+1):
    random.shuffle(road)
    dist = distance(road)
#    print("starting at: \t\t" + str(road) + "\t" + str(dist))
    i = random.randint(0, num_of_cities-2)
    while bad_cities > 0:
        new_road = move(road, i)
        temp_dist = distance(new_road)
        if temp_dist < dist:
            road = new_road
            dist = temp_dist
            bad_cities = num_of_cities/2
#            print("better road found: \t" + str(road) + "\t" + str(dist))
        else: 
            bad_cities -= 1
#            print("worse road found: \t" + str(new_road) + "\t" + str(temp_dist))
        i = random.randint(0, num_of_cities-2)
    if dist < ans_dist:
#        print("new best road")
        ans_road = road
        ans_dist = dist


# --------------
# end time
end = time.time()

# print
output = data[0][0]
for i in range (0, len(road)):
    output += " -> " + data[0][road[i]]
output += " -> " + data[0][0]
print(output)
print(ans_dist)
print("time elapsed: " + str(end - start))

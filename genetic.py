import csv
import itertools
import time
import random
import numpy
import matplotlib.pyplot as plt
with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))
num_of_cities = 24
pop_size = 2000
num_of_generations = 1000


class GeneticAlgorithm:
    def __init__(self, cities):
        self.mutation_prob = 0.05
        self.num_of_cities = cities

    class Road:
        # Saves the distance, and serves for better understanding of the code.
        # All permutations start in [0][0] "Barcelona"
        def __init__(self, permutation):
            self.road = tuple(permutation)
            self.dist = None

        def distance(self):
            if self.dist is not None:
                return self.dist
            points = (0,) + self.road + (0,)
            dist = 0
            for city in range (0, len(points)-1):
                dist += float(data[points[city]+1][points[city+1]])
            self.dist = dist
            return dist

        def __len__(self):
            return len(self.road)
        def __getitem__(self, index):
            return self.road[index]
        def __repr__(self):
            return str((0,)+ self.road +(0,))
        def index(self, something):
            return self.road.index(something)

    def road_sort(self,road: Road):
        # helping-function for sorting by fitness.
        return road.distance()

    def gen_population(self, popsize):
        # generates a population.
        population = []
        for i in range(0, popsize-1):
            person = [u for u in range(1, self.num_of_cities)]
            random.shuffle(person)
            population += [person]
        
        return population

    def pmx(self, parent1, parent2):
        # generic pmx algorithm.
        child = [None for i in range(len(parent1))]
        allele_size = random.randint(1, len(parent1)-1)
        start = random.randint(0, len(parent1)-1 - allele_size)
        
        for i in range(start, start + allele_size+1):
            child[i] = parent1[i]
        for i in range(start, start + allele_size+1):
            if parent2[i] in child:
                continue
            index = i
            while True:
                index = parent2.index(parent1[index])
                if start <= index <= start+allele_size:
                    continue
                child[index] = parent2[i]
                break
        for i in range(len(child)):
            if child[i] is None:
                child[i] = parent2[i]
        return child

    def crossover(self, parent1, parent2):
        # pmx for child, possibility for mutation
        child1 = self.pmx(parent1, parent2)
        if float(random.randint(0, 100)) /100 < self.mutation_prob:
            child1 = self.mutate(child1)
        child2 = self.pmx (parent2, parent1)
        if float(random.randint(0, 100)) /100 < self.mutation_prob:
            child2 = self.mutate(child2)
        return [child1, child2]

    def parentSelection(self, population):
        # TODO? this algorithm is selection, but 
        # should be upgraded to SUS or similar to choose more fit parents.
        children = list()
        # every parent-couple make 2 children.
        for i in range(0, int(len(population)/2)):
            children += [self.Road(i) for i in self.crossover(population[2*i], population[2*i +1])]
        population += children
        return population
        
    def mutate(self, child):
        # inversion mutation: invert a random segment. 
        segment_start = random.randint(0, len(child) -3)
        segment_end = random.randint(segment_start +1, len(child)-1)
        child[segment_start:segment_end] = reversed(child[segment_start:segment_end])

        return child

    def survivorSelection(self, population):
        # kills the least fit half of the population
        return [population[i] for i in range(0, 20)]

    def plot(self,):
    
        pops = [50, 100, 2000]
        # random population
        ret = []
        for pop in pops:
            ret1 = []
            population = self.gen_population(pop)
            population = [self.Road(i) for i in population]
            #sort for fitness
            population.sort(key=self.road_sort)

            for i in range(0, 1000):
                #new generation, population now doubled
                population = self.parentSelection(population)
                #half population
                population.sort(key=self.road_sort)
                population = self.survivorSelection(population)
                ret1+= [self.Road(population[0]).distance()]
            ret += [ret1]
        return ret

start = time.time()
ga = GeneticAlgorithm(num_of_cities)

#plotting:
ans = ga.plot()
x = range(0, 1000)
plt.plot(x, ans[0])
plt.plot(x, ans[1])
plt.plot(x, ans[2])
plt.legend([50,100,2000])
plt.xlabel('generation')
plt.ylabel('fitness (inverted)')
plt.title('difference in population size:')

# best of 20 runs
arr = [ans[2][999]]
for i in range (0, 20):
    ans = ga.plot()
    arr += [ans[2][999]]

# deviation
print("deviation: " + str(numpy.std(arr)))
# best
print("best: " + str(min(arr)))
# worst
print("worst: " + str(max(arr)))
# average
print("average length: " + str(numpy.average(arr)))
# graph
plt.show()

#time
end = time.time()

print("time elapsed: " + str(end - start))

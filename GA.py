import random
import timeit
import numpy as np
import csv


# GLOBAL PARAMETERS
# Maximum weight the knapsack bag can hold
MAX_WEIGHT = random.randint(10000, 20000)
MAX_SIZE = random.randint(10000, 20000)  # Maximum Size of the bag
NUMBER_OF_ITEMS = 20  # Total number of items available

POPULATION_SIZE = NUMBER_OF_ITEMS  # Population size of a generation
MUTATION_PROBABILITY = 0.3  # The Probability that the child will be mutated
CROSSOVER_PROBABILITY = 0.9  # Crossover about 90% of the time
NUMBER_OF_ITERATIONS = 300  # Total no of generations
seed = 1
TOTAL_WEIGHT_IN_BAG = 0
TOTAL_SIZE_OF_ITEMS_IN_BAG = 0
items = {}
Tournament_size = int(POPULATION_SIZE/4)
generate = True


def read():
    with open('Book1.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            if(i > 0):
                items[i-1] = row
                i += 1
            else:
                NUMBER_OF_ITEMS = row[0]
                MAX_WEIGHT = row[1]
                MAX_SIZE = row[2]
                i += 1

    for row in range(len(items)):
        for col in range(len(items[row])):
            items[row][col] = int(items[row][col])
        print(items[row])


def initialize_knapsack_table():
    """ Initializes Weight, Cost and Size """
    random_max_weight = 0
    random_max_size = 0
    random_max_cost = 0
    print("-------| Random Available Items |------- ")
    print("Num       W   C   S")

    for i in range(NUMBER_OF_ITEMS):
        weight_artifact = random.randint(
            1, int(MAX_WEIGHT/NUMBER_OF_ITEMS*10))  # Random Weight
        cost_artifact = random.randint(1, NUMBER_OF_ITEMS)  # Random Cost
        size_artifact = random.randint(
            1, int(MAX_SIZE/NUMBER_OF_ITEMS*10))  # Random Size
        # Store in Items variable
        items[i] = weight_artifact, cost_artifact, size_artifact
        print("Item {} : {}".format((i + 1), items[i]))  # Print to check data
        random_max_size += size_artifact  # Get Maximum of generated size
        random_max_weight += weight_artifact  # Get Maximum of generated Weight
        random_max_cost += cost_artifact
    print("Total Size: {}  Total Cost:{} Total Weight: {} ".format(
        random_max_size, random_max_cost, random_max_weight))

    ls = [NUMBER_OF_ITEMS, MAX_WEIGHT, MAX_SIZE]
    with open("Book1.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(ls)
    for i in range(NUMBER_OF_ITEMS):
        with open("Book1.csv", 'a+', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(items[i])


def print_knapsack_table():
    """ Prints the Table for final checkup """
    print("\n\n-------| Total Available Items |------- ")
    print("Num  weight  cost  size")
    for i in range(NUMBER_OF_ITEMS):
        print(chr(i + 65), end='     ')
        print(items[i][0], end='     ')
        print(items[i][1], end='     ')
        print(items[i][2])


class Individual:
    #  The individual holds a list of 0 or 1
    #  0 -  Item is not in Bag
    #  1 -  Item is there in Bag
    #  Stores fitness value of individual Chromosome

    def __init__(self):
        # Initializes the genome and fitness
        self.gene = []
        self.fitness = 0

    def generate(self):
        """ Generates random genomes for the first generation and calling fitness function """
        for i in range(NUMBER_OF_ITEMS):
            self.gene.append(random.randint(0, 1))
        self.fitness = self.fitness_function()

    def fitness_function(self):
        """ The fitness function gives the total value of the items in the knapsack
            If the weight exceeds the maximum weight fitness becomes 0"""
        fitness = 0
        weight = 0
        size_arti = 0
        for i in range(NUMBER_OF_ITEMS):
            if self.gene[i] == 1:
                weight += items[i][0]
                fitness += items[i][1]
                size_arti += items[i][2]
        if (weight > MAX_WEIGHT and size_arti < MAX_SIZE) or (weight < MAX_WEIGHT and size_arti > MAX_SIZE):
            fitness = int(fitness / 2)
        elif weight < MAX_WEIGHT and size_arti < MAX_SIZE:
            fitness = fitness
        elif weight > MAX_WEIGHT or size_arti > MAX_SIZE:
            fitness = 0
        return fitness

    """def mutate(self):
        for i in range(0, len(self.chromosome), 2):
            if choice(range(1, self.probabilty + 1)) == 1:
                if self.chromosome[i] == '1':
                    return Chromosome(self.chromosome[:i] + '00' + self.chromosome[i + 2:])
                elif self.chromosome[i] == '0':
                    return Chromosome(
                        self.chromosome[:i] + '1' + str(randint(1, RcParser().get_m())) + self.chromosome[i + 2:])
        return self.chromosome """

    def mutate(self):
        """ Chooses a random item and topples its presence """
        for i in range(seed):
            mutate_index = random.randint(0, NUMBER_OF_ITEMS - 1)
            self.gene[mutate_index] = bool(self.gene[mutate_index]) ^ 1
            self.fitness = self.fitness_function()


class Selection:
    def __init__(self, llist):
        self.populationlist = llist

    # populationlist[i].fitness
    def do_selection(self):
        # performs roulette selection
        fsum = 0
        pop_fsum = []
        for i in range(len(self.populationlist)):
            fitness = self.populationlist[i].fitness
            fsum = fsum + fitness
            pop_fsum.append(fitness)

        bound = random.uniform(0, fsum)
        curr_fsum = 0
        for i in range(len(self.populationlist)):
            curr_fsum = curr_fsum + pop_fsum[i]
            if curr_fsum >= bound:
                return self.populationlist[i]

    def tournament(self):
        # performs roulette selection
        tour_pop = []
        for i in range(Tournament_size):
            chromo = random.randint(0, POPULATION_SIZE - 1)
            tour_pop.append(chromo)

        maximum = 0
        for i in tour_pop:
            if self.populationlist[i].fitness > maximum:
                maximum = i

        return maximum


class Population:
    """ This stores a list of the population members of a generation"""

    def __init__(self):
        self.populationlist = []

    def generate_random_population(self):
        """ Generates a random list of population """
        for i in range(POPULATION_SIZE):
            chromosome = Individual()
            chromosome.generate()
            self.populationlist.append(chromosome)

    def sort_and_cut_growth(self):
        """ The population list is sorted according to the fitness function and the least fit ones are
            removed to maintain the population size """

        self.populationlist = sorted(
            self.populationlist, key=lambda x: x.fitness, reverse=True)
        self.populationlist = self.populationlist[:POPULATION_SIZE]

    def crossover(self):
        """ Randomly selects two individuls from population list and cross over happens
           It returns the two children """
        #crossover1 = random.randint(0, POPULATION_SIZE - 1)
        #crossover2 = random.randint(0, POPULATION_SIZE - 1)

        crossover1 = Selection(self.populationlist).tournament()
        crossover2 = Selection(self.populationlist).tournament()
        spiltpoint = random.randint(0, NUMBER_OF_ITEMS - 1)
        child1 = Individual()
        child2 = Individual()
        list1 = []
        list2 = []
        child1.gene = self.populationlist[crossover1].gene
        child2.gene = self.populationlist[crossover2].gene
        list1 = child1.gene[:spiltpoint] + child2.gene[spiltpoint:]
        list2 = child2.gene[:spiltpoint] + child1.gene[spiltpoint:]
        child1.gene = list1
        child2.gene = list2
        child1.fitness = child1.fitness_function()
        child2.fitness = child2.fitness_function()
        return child1, child2

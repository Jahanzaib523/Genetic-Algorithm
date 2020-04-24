import random
import timeit
import numpy as np
import csv
import matplotlib.pyplot as plt
from GA import *


def Draw_Mutation():
    MUTATION_PROBABILITY = 0.03
    llist1 = []
    llist2 = []
    llist3 = []
    for i in range(3):
        MUTATION_PROBABILITY += 0.3
        llist1.append(MUTATION_PROBABILITY)
        average = []
        weigh = []
        for j in range(5):
            tic = timeit.default_timer()
            read()
            knapsack = Population()
            # For first generation it is randomly populated
            knapsack.generate_random_population()
            condition = True
            z = 0
            while condition:
                TOTAL_WEIGHT_IN_BAG = 0
                TOTAL_SIZE_OF_ITEMS_IN_BAG = 0

                size = int(POPULATION_SIZE / 2 + 1)
                for y in range(size):  # Performs crossover
                    offspring1, offspring2 = knapsack.crossover()
                    if random.random() > MUTATION_PROBABILITY:  # if greater than given probability mutation occurs
                        offspring1.mutate()
                    if random.random() > MUTATION_PROBABILITY:
                        offspring2.mutate()
                    # After mutation it is appended to the list
                    knapsack.populationlist.append(offspring1)
                    knapsack.populationlist.append(offspring2)
                z += 1
                knapsack.sort_and_cut_growth()  # At the end of generation death cycle occurs
                for i in range(NUMBER_OF_ITEMS):  # Prints the solution set
                    if knapsack.populationlist[0].gene[i] == 1:
                        TOTAL_WEIGHT_IN_BAG = TOTAL_WEIGHT_IN_BAG + items[i][0]
                        TOTAL_SIZE_OF_ITEMS_IN_BAG = TOTAL_SIZE_OF_ITEMS_IN_BAG + \
                            items[i][2]

                rangerW = range(MAX_WEIGHT - 5, MAX_WEIGHT)
                rangerS = range(MAX_SIZE - 10, MAX_SIZE)

                if (TOTAL_WEIGHT_IN_BAG in rangerW) and (TOTAL_SIZE_OF_ITEMS_IN_BAG in rangerS):
                    condition = False
                elif z > NUMBER_OF_ITERATIONS:
                    condition = False
                elif TOTAL_WEIGHT_IN_BAG > MAX_WEIGHT or TOTAL_SIZE_OF_ITEMS_IN_BAG > MAX_SIZE:
                    condition = False
                else:
                    condition = True

            TOTAL_WEIGHT_IN_BAG = 0
            TOTAL_SIZE_OF_ITEMS_IN_BAG = 0
            for i in range(NUMBER_OF_ITEMS):  # Prints the solution set
                if knapsack.populationlist[0].gene[i] == 1:
                    TOTAL_WEIGHT_IN_BAG = TOTAL_WEIGHT_IN_BAG + items[i][0]
                    TOTAL_SIZE_OF_ITEMS_IN_BAG = TOTAL_SIZE_OF_ITEMS_IN_BAG + \
                        items[i][2]

            toc = timeit.default_timer()
            timetaken = (toc - tic)
            average.append(knapsack.populationlist[0].gene)
            weigh.append(TOTAL_WEIGHT_IN_BAG)
        llist2.append(average)
        llist3.append(weigh)

    for i in range(len(llist2)):
        for j in range(1, len(llist2[i])):
            for k in range(len(llist2[i][j])):
                llist2[i][0][k] = llist2[i][0][k]+llist2[i][j][k]
            llist3[i][0] += llist3[i][j]

    llist5 = []
    for i in range(len(llist3)):
        llist5.append(llist3[i][0]/5)

    llist4 = []
    for i in range(len(llist2)):
        for k in range(len(llist2[i][j])):
            llist2[i][0][k] /= 5
            if(llist2[i][0][k] > 0.5):
                llist2[i][0][k] = 1
            else:
                llist2[i][0][k] = 0
        llist4.append(llist2[i][0])

    plt.xlabel("Mutation probability")
    plt.ylabel("Weight ")

    plt.scatter(llist1, llist5)
    plt.plot(llist1, llist5)
    plt.show()


Draw_Mutation()


from GA import *

if __name__ == "__main__":
    tic = timeit.default_timer()

    if(generate):
        read()
    else:
        initialize_knapsack_table()  # Knapsack Table is got from the user
    knapsack = Population()
    # For first generation it is randomly populated
    knapsack.generate_random_population()
    condition = True
    z = 0
    while condition:
        TOTAL_WEIGHT_IN_BAG = 0
        TOTAL_SIZE_OF_ITEMS_IN_BAG = 0
        # Prints genome for each generation
        print("\nGeneration: {}".format((z + 1)))
        for i in range(POPULATION_SIZE):
            print("Genome: {}  Fitness : {}  ".format(knapsack.populationlist[i].gene,
                                                      knapsack.populationlist[i].fitness))
        size = int(POPULATION_SIZE * CROSSOVER_PROBABILITY)
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
        print("z: {} , Iteration : {}".format(z, NUMBER_OF_ITERATIONS))
        knapsack.sort_and_cut_growth()  # At the end of generation death cycle occurs
        for i in range(NUMBER_OF_ITEMS):  # Prints the solution set
            if knapsack.populationlist[0].gene[i] == 1:
                TOTAL_WEIGHT_IN_BAG = TOTAL_WEIGHT_IN_BAG + items[i][0]
                TOTAL_SIZE_OF_ITEMS_IN_BAG = TOTAL_SIZE_OF_ITEMS_IN_BAG + \
                    items[i][2]
        print("weight: {} , size : {}".format(
            TOTAL_WEIGHT_IN_BAG, TOTAL_SIZE_OF_ITEMS_IN_BAG))

        rangerW = range(MAX_WEIGHT - 5, MAX_WEIGHT)
        rangerS = range(MAX_SIZE - 10, MAX_SIZE)

        print("rangerW: {} , rangerS : {}".format(
            TOTAL_WEIGHT_IN_BAG in rangerW, TOTAL_SIZE_OF_ITEMS_IN_BAG in rangerS))

        if (TOTAL_WEIGHT_IN_BAG in rangerW) and (TOTAL_SIZE_OF_ITEMS_IN_BAG in rangerS):
            condition = False
            print("calling False")
        elif z > NUMBER_OF_ITERATIONS:
            condition = False
        elif TOTAL_WEIGHT_IN_BAG > MAX_WEIGHT or TOTAL_SIZE_OF_ITEMS_IN_BAG > MAX_SIZE:
            condition = False
        else:
            condition = True
            print("calling True")

    print_knapsack_table()

    print("\nBest Individual: {}".format(knapsack.populationlist[0].gene))
    TOTAL_WEIGHT_IN_BAG = 0
    TOTAL_SIZE_OF_ITEMS_IN_BAG = 0
    print("Items kept in the bag are: ", end='')
    for i in range(NUMBER_OF_ITEMS):  # Prints the solution set
        if knapsack.populationlist[0].gene[i] == 1:
            TOTAL_WEIGHT_IN_BAG = TOTAL_WEIGHT_IN_BAG + items[i][0]
            TOTAL_SIZE_OF_ITEMS_IN_BAG = TOTAL_SIZE_OF_ITEMS_IN_BAG + \
                items[i][2]
            print(chr(i + 65), end=' ')

    print("\nTotal Cost of Items in Bag: {}".format(
        knapsack.populationlist[0].fitness))
    print("Total weight of Items in Bag: {}".format(TOTAL_WEIGHT_IN_BAG))
    print("Total size of Items in Bag: {}".format(TOTAL_SIZE_OF_ITEMS_IN_BAG))
    toc = timeit.default_timer()
    timetaken = (toc - tic)
    print("Time taken : ", float("{0:.2f}".format(timetaken)))

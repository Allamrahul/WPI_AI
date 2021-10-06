import numpy as np
import random
import operator
import pandas as pd


class HillClimbingAlg:

    def __init__(self):
        pass

    @staticmethod
    def random_solution(tsp):
        cities = list(range(0, len(tsp)))
        solution = []

        for i in range(0, len(tsp)):
            random_city = cities[random.randint(0, len(cities) - 1)]
            solution.append(random_city)
            cities.remove(random_city)

        return solution

    @staticmethod
    def route_length(tsp, solution):
        route_len = 0

        for i in range(len(solution)):
            route_len += tsp[solution[i-1]][solution[i]]

        return route_len

    @staticmethod
    def get_neighbours(solution):
        neighbours = []

        for i in range(len(solution)):
            for j in range(i+1, len(solution)):
                neighbour = solution.copy()
                neighbour[i] = solution[j]
                neighbour[j] = solution[i]
                neighbours.append(neighbour)

        return neighbours

    @staticmethod
    def get_best_neighbour(tsp, neighbours):
        best_route_len = HillClimbingAlg.route_length(tsp, neighbours[0])
        best_neighbour = neighbours[0]

        for n in neighbours:
            current_route_len = HillClimbingAlg.route_length(tsp, n)

            if current_route_len < best_route_len:
                best_route_len = current_route_len
                best_neighbour = n

        return best_neighbour, best_route_len

    @staticmethod
    def step(tsp):
        current_solution = HillClimbingAlg.random_solution(tsp)
        current_route_length = HillClimbingAlg.route_length(tsp, current_solution)
        neighbours = HillClimbingAlg.get_neighbours(current_solution)

        best_neighbour, best_route_length = HillClimbingAlg.get_best_neighbour(tsp, neighbours)

        while best_route_length < current_route_length:
            current_solution = best_neighbour
            current_route_length = best_route_length
            neighbours = HillClimbingAlg.get_neighbours(current_solution)
            best_neighbour, best_route_length = HillClimbingAlg.get_best_neighbour(tsp, neighbours)

        print("The best path TSP can take is ", best_neighbour)
        print("The least route length is", best_route_length)


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    def routeDistance(self):
        if self.distance == 0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = self.route[i + 1] if (i + 1 < len(self.route)) else self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance

    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness


class GA:
    def __init__(self):
        pass

    @staticmethod
    def createRoute(cityList):
        route = random.sample(cityList, len(cityList))
        return route

    @staticmethod
    def initialPopulation(popSize, cityList):
        population = []

        for i in range(0, popSize):
            population.append(GA.createRoute(cityList))
        return population

    @staticmethod
    def rankRoutes(population):
        fitnessResults = {}
        for i in range(0, len(population)):
            fitnessResults[i] = Fitness(population[i]).routeFitness()
        return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)

    @staticmethod
    def selection(popRanked, eliteSize):
        selectionResults = []
        df = pd.DataFrame(np.array(popRanked), columns=["Index", "Fitness"])
        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

        for i in range(0, eliteSize):
            selectionResults.append(popRanked[i][0])
        for i in range(0, len(popRanked) - eliteSize):
            pick = 100 * random.random()
            for i in range(0, len(popRanked)):
                if pick <= df.iat[i, 3]:
                    selectionResults.append(popRanked[i][0])
                    break
        return selectionResults

    @staticmethod
    def matingPool(population, selectionResults):
        matingpool = []
        for i in range(0, len(selectionResults)):
            index = selectionResults[i]
            matingpool.append(population[index])
        return matingpool

    @staticmethod
    def breed(parent1, parent2):
        childP1 = []

        geneA = int(random.random() * len(parent1))
        geneB = int(random.random() * len(parent1))

        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        for i in range(startGene, endGene):
            childP1.append(parent1[i])

        childP2 = [item for item in parent2 if item not in childP1]

        child = childP1 + childP2
        return child

    @staticmethod
    def breedPopulation(matingpool, eliteSize):
        children = []
        length = len(matingpool) - eliteSize
        pool = random.sample(matingpool, len(matingpool))

        for i in range(0, eliteSize):
            children.append(matingpool[i])

        for i in range(0, length):
            child = GA.breed(pool[i], pool[len(matingpool) - i - 1])
            children.append(child)
        return children

    @staticmethod
    def mutate(individual, mutationRate):
        for swapped in range(len(individual)):
            if random.random() < mutationRate:
                swapWith = int(random.random() * len(individual))

                city1 = individual[swapped]
                city2 = individual[swapWith]

                individual[swapped] = city2
                individual[swapWith] = city1
        return individual

    @staticmethod
    def mutatePopulation(population, mutationRate):
        mutatedPop = []

        for ind in range(0, len(population)):
            mutatedInd = GA.mutate(population[ind], mutationRate)
            mutatedPop.append(mutatedInd)
        return mutatedPop

    @staticmethod
    def nextGeneration(currentGen, eliteSize, mutationRate):
        popRanked = GA.rankRoutes(currentGen)
        selectionResults = GA.selection(popRanked, eliteSize)
        matingpool = GA.matingPool(currentGen, selectionResults)
        children = GA.breedPopulation(matingpool, eliteSize)
        nextGeneration = GA.mutatePopulation(children, mutationRate)
        return nextGeneration

    @staticmethod
    def step(population, popSize, eliteSize, mutationRate, generations):
        pop = GA.initialPopulation(popSize, population)
        print("Population: ", pop)
        print("Initial distance: " + str(1 / GA.rankRoutes(pop)[0][1]))

        for i in range(0, generations):
            pop = GA.nextGeneration(pop, eliteSize, mutationRate)

        print("Final distance: " + str(1 / GA.rankRoutes(pop)[0][1]))
        bestRouteIndex = GA.rankRoutes(pop)[0][0]
        bestRoute = pop[bestRouteIndex]
        return bestRoute

    @staticmethod
    def prepare_input(num_cities):
        cityList = []
        for i in range(0, num_cities):
            cityList.append(City(x=int(random.random() * 200), y=int(random.random() * 200)))

        return cityList


def genetic_algorithm(num_cities):
    print("-----------------------Executing genetic algorithm for TSP-------------------\n")

    cityList = GA.prepare_input(num_cities)
    print("City list : ", cityList)
    print("Final path: ", GA.step(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500))


def hill_climbing_alg():
    #  represents 4 cities(0, 1, 2, 3) and distances between them in the form of a grid
    tsp = [
        [0, 400, 500, 300],
        [400, 0, 300, 500],
        [500, 300, 0, 400],
        [300, 500, 400, 0]
    ]

    print("-----------------------Executing hill climbing algorithm for TSP---------------\n")

    print("Input city list", tsp)

    HillClimbingAlg.step(tsp)


"""

Assumptions: 

1. For the hill climbing algorithm implementation, I have assumed 4 cities and assigned random distances to it
2. For the genetic algorithm implementation, I have assumed the presence of 10 cities and the following are the other parameter
assumptions: popSize=100, eliteSize=20, mutationRate=0.01, generations=500


"""


def main():
    hill_climbing_alg()
    genetic_algorithm(num_cities=10)


if __name__ == "__main__":
    main()

import random


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

        print(best_neighbour)
        print(best_route_length)


def main():

    tsp = [
        [0, 400, 500, 300],
        [400, 0, 300, 500],
        [500, 300, 0, 400],
        [300, 500, 400, 0]
    ]

    HillClimbingAlg.step(tsp)


if __name__ == "__main__":
    main()

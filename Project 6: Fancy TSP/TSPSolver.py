#!/usr/bin/python3
import signal
from random import randint

from proj5.GeneticClasses import Solution, Population
from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
    from PyQt6.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time
import numpy as np
from TSPClasses import *
import heapq
import itertools


class TimeoutException(Exception):
    pass


def timeout_handler():
    raise TimeoutException("Reached time limit.")


class TSPSolver:
    def __init__(self, gui_view):
        self._scenario = None

    def setupWithScenario(self, scenario):
        self._scenario = scenario

    ''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

    def defaultRandomTour(self, time_allowance=60.0):
        # signal.signal(signal.SIGALRM, timeout_handler())
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None
        start_time = time.time()
        # signal.setitimer(signal.ITIMER_REAL, time_allowance)
        while not foundTour and time.time() - start_time < time_allowance:
            # create a random permutation
            perm = np.random.permutation(ncities)
            route = []
            # Now build the route using the random permutation
            for i in range(ncities):
                route.append(cities[perm[i]])
            bssf = TSPSolution(route)
            count += 1
            if bssf.cost < np.inf:
                # Found a valid route
                foundTour = True
        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    ''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

    def greedy(self, time_allowance=60.0):
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        count = 0
        bssf = None
        foundTour = True
        start_time = time.time()
        # Implement greedy algorithm.
        for startCity in cities:
            foundTour = False
            currentCity = startCity
            route = [startCity]
            # Loop over each city in the tour.
            while not foundTour and time.time() - start_time < time_allowance:
                # Take the shortest path to a city that has not been visited yet (and is not the starting city).
                # Find the closest unvisited city
                closestCity = startCity
                distanceToClosestCity = currentCity.costTo(closestCity)
                for nextCity in cities:
                    # if the chosen city has not been visited yet
                    if nextCity not in route:
                        # check to see if it is the closest such city.
                        distanceToNextCity = currentCity.costTo(nextCity)
                        if closestCity == startCity:
                            closestCity = nextCity
                        elif distanceToNextCity < distanceToClosestCity:
                            closestCity = nextCity
                        distanceToClosestCity = currentCity.costTo(closestCity)
                # Once each city has been tested for closeness,
                # the closest city is either the next step in the path...
                if closestCity != startCity:
                    route.append(closestCity)
                    currentCity = closestCity
                # ...or the starting city.
                else:
                    foundTour = True
                    newSolution = TSPSolution(route)
                    if bssf is None or (newSolution is not None and newSolution.cost < bssf.cost):
                        bssf = newSolution
                    count += 1
            if time.time() - start_time >= time_allowance:
                break
        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results


    ''' <summary>
        This is the entry point for the branch-and-bound algorithm that you will implement
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of best solution,
        time spent to find best solution, total number solutions found during search (does
        not include the initial BSSF), the best solution found, and three more ints:
        max queue size, total number of states created, and number of pruned states.</returns>
    '''


    def branchAndBound(self, time_allowance=60.0):
        # signal.signal(signal.SIGALRM, timeout_handler())
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None
        start_time = time.time()
        # signal.setitimer(signal.ITIMER_REAL, time_allowance)
        while not foundTour and time.time() - start_time < time_allowance:
            # create a random permutation
            perm = np.random.permutation(ncities)
            route = []
            # Now build the route using the random permutation
            for i in range(ncities):
                route.append(cities[perm[i]])
            bssf = TSPSolution(route)
            count += 1
            if bssf.cost < np.inf:
                # Found a valid route
                foundTour = True
        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results


    ''' <summary>
        This is the entry point for the algorithm you'll write for your group project.
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of best solution,
        time spent to find best solution, total number of solutions found during search, the
        best solution found.  You may use the other three field however you like.
        algorithm</returns>
    '''


    def fancy(self, time_allowance=60.0):
        start_time = time.time()

        num_generations = 50
        population_size = 20
        new_random_per_generation = math.ceil(population_size * .10)  # number of new solutions to be generated via mutation
        crossover_per_generation = math.ceil(
            population_size * .60)  # number of new solutions to be generated via crossing over
        mutation_rate = 30  # percent chance to create a new solution via mutation
        population_holdover = population_size  # number of old solutions to keep in new population

        # generate starting population based on a greedy algorithm and many random
        greedy_path = self.greedy()['soln'].route
        greedy_solution = Solution(greedy_path)
        population = Population()
        population.addSolution(greedy_solution)

        while population.getSize() < population_size:
            new_random = self.defaultRandomTour()['soln'].route
            random_solution = Solution(new_random)
            population.addSolution(random_solution)
            if (time.time() - start_time > time_allowance):
                print("Broke while making population")
                break

        for i in range(num_generations):
            if (time.time() - start_time > time_allowance):
                break
            new_population = Population()
            x = slice(0, population_holdover)
            for solution in population.getSolutions()[x]:
                new_population.addSolution(solution)
            # cross over two existing solutions and add to new population
            for j in range(crossover_per_generation):
                solution1 = population.selectSolution()
                solution2 = population.selectSolution()
                cross_path = CrossOver(solution1, solution2)
                cross_solution = Solution(cross_path)
                new_population.addSolution(cross_solution)
            # create new random solutions and add to new population to help escape local minima
            for j in range(new_random_per_generation):
                new_random = self.defaultRandomTour()['soln'].route
                random_solution = Solution(new_random)
                new_population.addSolution(random_solution)
            # mutate existing solutions at random and add to new population
            for solution in population.getSolutions():
                new_path = Mutate(solution, mutation_rate)
                new_solution = Solution(new_path)
                new_population.addSolution(new_solution)
            new_population.cull(50)
            population = new_population
            if (time.time() - start_time > time_allowance):
                print("ran out of time in the algorithm")
                break
        final_solution = population.getBestSolution()
        end_time = time.time()
        bssf = TSPSolution(final_solution.getPath())
        results = {}
        results['cost'] = bssf.cost
        results['time'] = end_time - start_time
        results['count'] = 1
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

def Mutate(solution, mutation_rate):
    path = solution.getPath()
    if randint(0, 100) < mutation_rate:
        index_1 = randint(0, len(path) - 1)
        index_2 = randint(0, len(path) - 1)
        city1 = path[index_1]
        path[index_1] = path[index_2]
        path[index_2] = city1
    #returns original solution if mutation failed
    #could potentially check solution fitness before adding to prevent duplicates
    #will still have to check for duplicates regardless?
    return path

def CrossOver(solution1, solution2):
    path1 = solution1.getPath()
    path2 = solution2.getPath()
    cut1 = randint(0, len(path1) - 1)
    cut2 = randint(cut1-1, len(path2) - 1)
    cross_path = path1[cut1:cut2]
    for i in range(len(path2)):
        city = path2[i]
        if city not in cross_path:
            cross_path.append(city)
    return cross_path
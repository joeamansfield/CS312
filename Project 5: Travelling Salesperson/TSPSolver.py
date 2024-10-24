#!/usr/bin/python3

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
import copy
from CrossOver import CrossOver
from Mutate import Mutate



class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
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

	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
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

	def greedy( self,time_allowance=60.0 ):
		pass



	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''

	def branchAndBound( self, time_allowance=60.0 ):
		pass



	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
	'''

	def fancy( self,time_allowance=60.0 ):
		start_time = time.time()

		num_generations = 10
		population_size = 50
		new_random_per_generation = math.ceil(population_size * .10)#number of new solutions to be generated via mutation
		crossover_per_generation = math.ceil(population_size * .60) #number of new solutions to be generated via crossing over
		mutation_rate = 30 #percent chance to create a new solution via mutation
		population_holdover = population_size #number of old solutions to keep in new population


		#generate starting population based on a greedy algorithm and many random
		greedy_path = greedy()['soln'].route
		greedy_solution = Solution(greedy_path)
		population = Population()
		population.addSolution(greedy_solution)
		while population.getSize() < population_size:
			new_random = self.defaultRandomTour()['soln'].route
			random_solution = Solution(new_random)
			population.addSolution(random_solution)

		new_population = Population()
		for solution in population.getSolutions()[0, population_holdover]:
			new_population.addSolution(solution)

		for i in range(num_generations):
			#cross over two existing solutions and add to new population
			for j in range(crossover_per_generation):
				solution1 = population.selectSolution()
				solution2 = population.selectSolution()
				cross_path = CrossOver(solution1, solution2)
				cross_solution = Solution(cross_path)
				new_population.addSolution(cross_solution)
			#create new random solutions and add to new population to help escape local minima
			for j in range(new_random_per_generation):
				new_random = self.defaultRandomTour()['soln'].route
				random_solution = Solution(new_random)
				new_population.addSolution(random_solution)
			#mutate existing solutions at random and add to new population
			for solution in population.getSolutions():
				path = solution.getPath()
				new_path = Mutate(path, mutation_rate)
				new_solution = Solution(new_path)
				new_population.addSolution(new_solution)
			population = new_population.cull(50)
		final_solution = population.getBestSolution()
		end_time = time.time()
		bssf = TSPSolution(final_solution.getPath())
		results = {}
		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = None
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results

		#Population functions
		#selectSolution - returns solution based on probabilities https://www.youtube.com/watch?v=ETphJASzYes

		#finishing solution class by overloading functions
		#addSolution - adds solution iff it is unique and fitness > 0
		#getSolutions - returns list with all solutions
		#getBestSolution - returns best solution
		#getSize - returns size of solutions list

		#cull - removes all but the x best solutions

		#Population class will contain a member that is an ordered list of solutions named "solutions"


	def cull(self, size):
		self.solutions.sort()
		self.solutions = self.solutions[0,populationSize]
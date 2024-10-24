import copy
import random

import numpy as np

from proj5.TSPClasses import TSPSolution


class Population:
    def __init__(self):
        self.fitnessSum = 0
        self.solutions = []

    def addSolution(self, solution):
        for x in self.solutions:
            if x == solution or solution.fitness == 0:
                return
        self.solutions.append(solution)

    def getSolutions(self):
        self.solutions.sort(reverse=True)
        return self.solutions

    def selectSolution(self):
        self.solutions.sort(reverse=True)
        self.calculateFitnessSum()
        index = 0
        rndm = random.uniform(0, self.fitnessSum)

        while rndm > 0:
            rndm = rndm - self.solutions[index].fitness
            index = index + 1

        index = index - 1

        return self.solutions[index]

    def cull(self, populationSize):
        self.solutions.sort(reverse=True)
        x = slice(0, populationSize)
        self.solutions = self.solutions[x]

    def getBestSolution(self):
        self.solutions.sort(reverse=True)
        return self.solutions[0]

    def getSize(self):
        return len(self.solutions)

    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for solution in self.solutions:
            self.fitnessSum += solution.fitness


class Solution:
    def __init__(self, path):
        self.path = path
        self.cost = TSPSolution(path).cost
        if self.cost < np.inf:
            self.fitness = 1 / self.cost
        else:
            self.fitness = 0

    def getPath(self):
        result = []
        for city in self.path:
            result.append(city)
        return result

    def __eq__(self, other):
        return isinstance(other, Solution) and other.path == self.path

    def __lt__(self, other):
        return self.fitness < other.fitness


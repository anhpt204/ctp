#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import array
import random
import json

import numpy
import operator

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from problem import CTPProblem
from os.path import join

from setting import *
from deap.algorithms import varAnd
from crossovers import PMX, vrpPMX, scpOnePointCX, vrpOnePointCX
from genetic import varAndLS, varAndVRP
from mutations import mutLS, mutLS4, mutLSVRP, repair
from datetime import timedelta
import gcsp
from copy import deepcopy


class GA_VRP:
    '''
    GA for Vehicle Routing Problem
    '''
    
    def __init__(self, problem, nodes):
        '''
        @param problem: problem
        @param nodes: list of nodes
        '''
        self.toolbox = base.Toolbox()
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin, giant_tour=list, tours=list)
        
        current_gen = 0
        self.problem = problem
        self.nodes = nodes
        
        self.POPSIZE=20
        self.NUMGEN=50
        self.INDSIZE = len(nodes)
        self.VERBOSE=True
        self.PMUTATION = 0.3
        self.PCROSS = 1.0
        self.init_pop={}
        
        self.initialize()

    def ind_init(self):
        '''
        khoi tao individuals = hoan vi cua cac node trong nodes
        '''            
#         ind= random.sample(self.nodes, self.INDSIZE)
    
        # replace a node in nodes with another node
        len_T = len(self.problem.obligatory_nodes)
        
        l = 0
        while l < 100:
            l += 1
            ind = self.toolbox.clone(self.nodes)
            # choice a node in individual that not in T
            idx = random.choice(range(len(ind)))
            while ind[idx] < len_T:
                idx = random.choice(range(len(ind)))
            
            covering_set = set()
            for i in xrange(len(ind)):
                if i != idx:
                    covering_set.update(self.problem.get_set_of_customers_covered_by(ind[i]))
            
            found = False
            for node_j in self.problem.nodes:
                # if node_j in T
                if node_j < len_T:
                    continue
                
                c = covering_set.union(self.problem.get_set_of_customers_covered_by(node_j.id))
                
                if len(c) == self.problem.num_of_customers: # satisfy covering constraint
                    ind[idx] = node_j.id
                
                    # if have the same node    
                    if len(ind) > len(set(ind)):
                        continue
                    
                    key=tuple(ind)
                    if not self.init_pop.has_key(key):
                        self.init_pop[key]=1
                        found = True
                        break
            if found:
                break
        if found:
            return random.sample(ind, len(ind))
        else:
            return random.sample(self.nodes, self.INDSIZE)
    
    def initialize(self):
        
        self.toolbox.register("indices", self.ind_init)
        
        
        
        # Structure initializers
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.indices)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("mate", vrpPMX)#PMX)
    #     tools.cxPartialyMatched(ind1, ind2)
        self.toolbox.register("ls", mutLSVRP, problem=self.problem)
#         self.toolbox.register("ls4", mutLS4, problem=problem)
#         self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=INDPB)
        self.toolbox.register("pop_repair", repair, self.problem)
        
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", self.eval)
                                    
    # evaluate solution
    def eval(self, individual):
#         print individual
        
        cost, backtrack = self.problem.split(individual)
                
        # split tour and return total cost
        tour = [node for node in individual]
        individual.tours = self.problem.extract_tours(tour, backtrack)
            
        return cost,
    
    
    def evolve(self, population, toolbox, cxpb, mutpb, ngen, stats=None, sizeStats=None,
                 halloffame=None, verbose=__debug__):
        global current_gen
        
        logbook = tools.Logbook()
        logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
    
        if halloffame is not None:
            halloffame.update(population)
    
        record = stats.compile(population) if stats else {}
#         record.update(sizeStats.compile(population) if sizeStats else {})
        
        logbook.record(gen=0, nevals=len(invalid_ind),**record)
        
        if verbose:
            print logbook.stream
        best_ind=None
        # Begin the generational process
        for gen in range(1, ngen+1):
            current_gen = gen
            # Select the next generation individuals
            offspring = toolbox.select(population, len(population))
            
            # Vary the pool of individuals
            offspring = varAndVRP(offspring, self.toolbox, cxpb, mutpb, gen)
            #repairing
            offspring = toolbox.map(toolbox.pop_repair, offspring) 
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
                
            # Replace the current population by the offspring
            population[:] = offspring
            
             # elitism
            t = random.randint(0, len(population)-1)
    #         t = 0
            if best_ind:
                population[t] = best_ind

            # Update the hall of fame with the generated individuals
            if halloffame is not None:
                halloffame.update(population)
            
            min_cost=10**100
            for ind in population:
                if ind.fitness.values[0] < min_cost:
                    min_cost = ind.fitness.values[0]
                    best_ind=deepcopy(ind)
                    
            # Append the current generation statistics to the logbook
            record = stats.compile(population) if stats else {}
#             record.update(sizeStats.compile(population) if sizeStats else {})
            
            logbook.record(gen=gen, nevals=len(invalid_ind), **record)
            if verbose:
                print logbook.stream        
    
        return population, logbook
    
    
    def run(self, job=0):
        random.seed(1000+job)
    
        pop = self.toolbox.population(n=self.POPSIZE)
    
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        
#         sizeStats = tools.Statistics(lambda ind: len(ind.giant_tour))
#         sizeStats.register('size_avg', numpy.mean)
        
        self.evolve(population=pop, 
               toolbox=self.toolbox, cxpb=self.PCROSS, mutpb=self.PMUTATION, 
               ngen=self.NUMGEN, stats=stats, halloffame=hof, verbose=self.VERBOSE)
        
#         print 'run ', job, ': ', hof[0].fitness.values[0], ': ', problem.best_cost, ': ', problem.n_same_giant_tour
    
    #     print hof[0].giant_tour
    #     print hof[0].tours
    #     calculate_tours_cost(problem, hof[0].tours, job)
    
        return hof[0].fitness.values[0], hof[0]

import glob, os, datetime
if __name__ == "__main__":
    # load problem
    folder = 'A'
    data_dir = 'data/' + folder + '/'
    print data_dir
#     Jobs = 10
    
    files = glob.glob(data_dir + '*.ctp')
    lines = []
    
    files = [os.path.join(data_dir, 'A-75-75-4.ctp')]
#     files = [os.path.join(data_dir, 'A-50-50-6.ctp')]
    moves_freq = {}
    
    for file in files:
        time1 = datetime.datetime.now()
        file_name = os.path.basename(file)
        print file_name
        
#         problem = CTPProblem(data_path=file)
        
        problem = gcsp.GCSPProblem(data_path=file)
        
        # calculate solution cost
#         tours = [[72,67,28,24], [5,48,52,18]]
#         cost = problem.get_solution_cost(tours)
#         print cost
#         break
        nodes = [2,3,4,5,8,9,6]
        ga = GA_VRP(problem, nodes)
        ga.run(0)
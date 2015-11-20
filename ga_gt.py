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
from crossovers import PMX, vrpPMX, scpOnePointCX
from genetic import varAndLS, varAndVRP, varAndSCP
from mutations import mutLS, mutLS4, mutLSVRP
from datetime import timedelta
import gcsp
from ga_vrp import GA_VRP
from hoang import ELS
from copy import deepcopy


class GA_GT:
    '''
    GA for CTP with individual = giant tour
    '''
    
    def __init__(self, problem):
        '''
        @param problem: problem
        @param nodes: list of nodes
        '''
        self.toolbox = base.Toolbox()
        creator.create("FitnessMin1", base.Fitness, weights=(-1.0,))
        creator.create("Individual1", array.array, typecode='i', fitness=creator.FitnessMin1, tours=list)
        
        current_gen = 0
        self.problem = problem
        
        self.POPSIZE=20
        self.NUMGEN=20
        self.INDSIZE = self.problem.num_of_nodes + len(self.problem.obligatory_nodes)
        self.cxP=0.6
        self.mutP=1.0/self.INDSIZE
        self.init_popsize=0
        
        self.initialize(problem.name)
        
        # for testing only
        self.best_cost = 10**10
        # job, gen
        self.stats = []
        
    def pop_ctp_init(self):
        '''
        khoi tao individual cho bai m-CTP-p cua Hoang
        '''
        selected_nodes =[]
        unselected_nodes=[x for x in xrange(max(self.problem.obligatory_nodes) + 1, max(self.problem.obligatory_nodes) + self.problem.num_of_nodes+1)]
        uncovered_customers = set(xrange(self.problem.num_of_customers))
        covering_set=set()

        # randomly select a start node
        node=random.choice(unselected_nodes)
        unselected_nodes.remove(node)
        selected_nodes.append(node)
        covering_set.update(self.problem.get_set_of_customers_covered_by(node))
        uncovered_customers.difference_update(self.problem.get_set_of_customers_covered_by(node))

        max_num_covered_customers=0
        max_node=-1

        # get a set that covers all customers        
        while len(covering_set) != self.problem.num_of_customers:
            for node in unselected_nodes:
                covered_customers = self.problem.get_set_of_customers_covered_by(node)
                tmp=uncovered_customers.intersection(covered_customers)
                if len(tmp) > max_num_covered_customers:
                    max_num_covered_customers=len(tmp)
                    max_node=node
            
            selected_nodes.append(max_node)
            unselected_nodes.remove(max_node)
            uncovered_customers.difference_update(self.problem.get_set_of_customers_covered_by(max_node))
            covering_set.update(self.problem.get_set_of_customers_covered_by(max_node))
            max_num_covered_customers=0
            
        # remove redundant nodes
        ind=self.problem.remove_node(selected_nodes)
        
        binary_ind = [0]*self.INDSIZE
        for i in ind:
            binary_ind[i-1]=1
        for i in self.problem.obligatory_nodes:
            binary_ind[i-1]=1
        return binary_ind
        
    def pop_gcsp_init(self):
        '''
        khoi tao individual cho bai m-CTP-p cua Hoang
        '''
        selected_nodes =[]
        unselected_nodes=[x for x in xrange(1, self.problem.num_of_nodes)]
        uncovered_customers = set(xrange(self.problem.num_of_customers))
        covering_set=set()

        # randomly select a start node
        node=random.choice(unselected_nodes)
        unselected_nodes.remove(node)
        selected_nodes.append(node)
        covering_set.update(self.problem.get_set_of_customers_covered_by(node))
        uncovered_customers.difference_update(self.problem.get_set_of_customers_covered_by(node))

        max_num_covered_customers=0
        max_node=-1

        # get a set that covers all customers        
        while len(covering_set) != self.problem.num_of_customers:
            for node in unselected_nodes:
                covered_customers = self.problem.get_set_of_customers_covered_by(node)
                tmp=uncovered_customers.intersection(covered_customers)
                if len(tmp) > max_num_covered_customers:
                    max_num_covered_customers=len(tmp)
                    max_node=node
            
            selected_nodes.append(max_node)
            unselected_nodes.remove(max_node)
            uncovered_customers.difference_update(self.problem.get_set_of_customers_covered_by(max_node))
            covering_set.update(self.problem.get_set_of_customers_covered_by(max_node))
            max_num_covered_customers=0
            
        # remove redundant nodes
        ind=self.problem.remove_node(selected_nodes)
        
        binary_ind = [0]*self.INDSIZE
        for i in ind:
            binary_ind[i-1]=1
        for i in self.problem.obligatory_nodes:
            binary_ind[i-1]=1
        return binary_ind
        
        
        
    def ind_init(self):
        '''
        khoi tao individuals = hoan vi cua cac node trong nodes
        '''            
#         return random.sample(self.nodes, self.INDSIZE)
        ind=[]
        # w[i]=the number of columms that cover row i
        w=[0]*self.problem.num_of_customers
        for c in xrange(self.problem.num_of_customers):
            # randomly select a node that covers customer c
            node = random.choice(tuple(self.problem.nodes_covering_customer[c]))
            ind.append(node)
            for i in self.problem.get_set_of_customers_covered_by(node):
                w[i]+=1
            
        # remove redundant node
        T = ind[:]
        while len(T) > 0:
            j = random.choice(T)
            T.remove(j)
            temp=True
            for i in self.problem.get_set_of_customers_covered_by(j):
                if w[i]<2:
                    temp=False
                    break
            if temp:
                ind.remove(j)
                for i in self.problem.get_set_of_customers_covered_by(j):
                    w[i] = w[i]-1
        
                    
        for i in xrange(len(self.problem.obligatory_nodes)):
            index = random.randint(0, len(ind)-1)
            ind.insert(index, i+1)
            
        return ind
        
    
    def init_mip(self):
        '''
        Khoi tao SCP tu MIP
        '''
        nodes = self.lines[2*self.init_popsize+1].split()
        nodes = [int(v) for v in nodes]
        
        return nodes
        
        
    def initialize(self, problem_name):
        
        self.toolbox.register("indices", self.ind_init)
        
#         self.toolbox.register("indices", self.init_mip)
        
        
        # Structure initializers
        self.toolbox.register("individual", tools.initIterate, creator.Individual1, self.toolbox.indices)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("mate", tools.cxESTwoPoint)
#         tools.cxPartialyMatched(ind1, ind2)
#         self.toolbox.register("ls", mutLSVRP, problem=problem)
#         self.toolbox.register("ls4", mutLS4, problem=problem)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", self.eval)
        
        mip_data_dir = 'SubSet'
        self.lines = open(join(mip_data_dir, problem_name),'r').readlines()

                                    
    # evaluate solution
    def eval(self, individual):
        giant_tour = [node for node in individual]
                
        if not individual.fitness.valid:
            cost, backtrack = problem.split(giant_tour)
            individual.fitness.values = cost,
            individual.tours = problem.extract_tours(giant_tour, backtrack)
            
        new_giant_tour, new_tours, new_cost = ELS(self.problem, giant_tour, individual.tours, individual.fitness.values[0])
                            
        if new_cost < self.best_cost:
            self.best_cost = new_cost
        print new_cost, self.best_cost
        
        individual.tours = new_tours
        
        N = len(new_giant_tour)
        if N < len(individual):
            del individual[len(new_giant_tour)]
            
        assert len(individual)==N, 'len individual is not equal N'
        for i in xrange(N):
            individual[i]=new_giant_tour[i]
        
        return new_cost,
    
    def repair_ind(self, ind):

        giant_tour = [i for i in ind]
        if not self.problem.is_giant_tour_satisfy_covering_constraint(giant_tour):
            # try until find feasible giant tour
            while True:
                nodes_in_giant_tour = set(giant_tour)
                nodes_not_in_giant_tour = set(range(1, len(problem.nodes))).difference(nodes_in_giant_tour)
                
                nodes_not_in_giant_tour = list(nodes_not_in_giant_tour)
                
                covering_set = problem.get_set_of_customers_covered_by_giant_tour(giant_tour)
                
                max_node = nodes_not_in_giant_tour[0]
                new_covering_set = covering_set.union(problem.get_set_of_customers_covered_by(max_node))
                max_covered = len(new_covering_set)
                for node in nodes_not_in_giant_tour[1:]:
                    new_covering_set = covering_set.union(problem.get_set_of_customers_covered_by(node))
                    if len(new_covering_set) > max_covered:
                        max_covered = len(new_covering_set)
                        max_node = node
                        
                # insert max_node into giant tour at random position
                idx = random.randint(0, len(giant_tour))
                giant_tour.insert(idx, max_node)
                
                # if is feasible giant tour then break while loop
                if problem.is_giant_tour_satisfy_covering_constraint(giant_tour):
                    break
        # remove redundent nodes
        giant_tour = problem.remove_node(giant_tour)

        # update individual
        new_ind = deepcopy(ind)
        
        del new_ind[:]
        for node in giant_tour:
            new_ind.append(node)
        
        cost, backtrack = problem.split(giant_tour)
        new_ind.fitness.values = cost,
        new_ind.tours = problem.extract_tours(giant_tour, backtrack)
                                                
        return new_ind
        
    def varAndPTA(self, population):
        
        offspring = [self.toolbox.clone(ind) for ind in population]
        
        # Apply crossover and mutation on the offspring
        for i in range(1, len(offspring), 2):
            if random.random() < self.cxP:
                offspring[i-1], offspring[i] = self.toolbox.mate(offspring[i-1], offspring[i])
                del offspring[i-1].fitness.values, offspring[i].fitness.values
                
                # repair
                offspring[i-1] = self.repair_ind(offspring[i-1])
                offspring[i] = self.repair_ind(offspring[i])
        
#         for i in range(len(offspring)):
#             if random.random() < self.mutP:
#                 offspring[i], = self.toolbox.mutate(offspring[i])
#                 del offspring[i].fitness.values
        
            
        return offspring
            
        
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
        
        # Begin the generational process
        for gen in range(1, ngen+1):
            current_gen = gen
            # Select the next generation individuals
            offspring = toolbox.select(population, len(population))
            
            # Vary the pool of individuals
            offspring = self.varAndPTA(offspring)
                        
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            # Update the hall of fame with the generated individuals
            if halloffame is not None:
                halloffame.update(offspring)
                
            # Replace the current population by the offspring
            population[:] = offspring
            
             # elitism
            t = random.randint(0, len(population)-1)
    #         t = 0
            population[t] = halloffame[0]
            
            # Append the current generation statistics to the logbook
            record = stats.compile(population) if stats else {}
#             record.update(sizeStats.compile(population) if sizeStats else {})
            
            logbook.record(gen=gen, nevals=len(invalid_ind), **record)
            if verbose:
                print logbook.stream        
    
#             print halloffame[0].tours
            
        return population, logbook
    
    
    def run(self, job=0):
        random.seed(1000+job)
    
#         POPSIZE= 200 #len(self.lines)/2
        
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
               toolbox=self.toolbox, cxpb=self.cxP, mutpb=0.3, 
               ngen=self.NUMGEN, stats=stats, halloffame=hof, verbose=VERBOSE)
        
        print 'run ', job, ': ', hof[0].fitness.values[0], ': ', problem.best_cost, ': ', problem.n_same_giant_tour
    
    #     print hof[0].giant_tour
    #     print hof[0].tours
    #     calculate_tours_cost(problem, hof[0].tours, job)
    
        return hof[0]

import glob, os, datetime
if __name__ == "__main__":
    # load problem
    folder = 'A'
    data_dir = 'data_ctp/' + folder + '/'
    print data_dir
#     Jobs = 10
    
    files = glob.glob(data_dir + '*.ctp')
    lines = []
    
    files = [
             
#             os.path.join(data_dir, 'A1-1-25-75-4.ctp'),
#             os.path.join(data_dir, 'A1-1-25-75-5.ctp'),
#             os.path.join(data_dir, 'A1-1-25-75-6.ctp'),
#             os.path.join(data_dir, 'A1-1-25-75-8.ctp'),

#             os.path.join(data_dir, 'A2-20-100-100-4.ctp'),
#              os.path.join(data_dir, 'A2-20-100-100-5.ctp'),
            os.path.join(data_dir, 'A2-20-100-100-6.ctp'),
#              os.path.join(data_dir, 'A2-20-100-100-8.ctp'),
#              os.path.join(data_dir, 'B2-20-100-100-4.ctp'),
#              os.path.join(data_dir, 'B2-20-100-100-5.ctp'),
#              os.path.join(data_dir, 'B2-20-100-100-6.ctp'),
#              os.path.join(data_dir, 'B2-20-100-100-8.ctp'),
             ]
#     files = [os.path.join(data_dir, 'A-50-50-6.ctp')]
    moves_freq = {}
    
    for file in files:
        time1 = datetime.datetime.now()
        file_name = os.path.basename(file)
        print file_name
        
        problem = CTPProblem(data_path=file)
        
#         problem = gcsp.GCSPProblem(data_path=file)
        
        # calculate solution cost
#         tours = [[72,67,28,24], [5,48,52,18]]
#         cost = problem.get_solution_cost(tours)
#         print cost
#         break
        ga = GA_GT(problem)
        solution = ga.run(0)
        
        print solution
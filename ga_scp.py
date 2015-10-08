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


class GA_SCP:
    '''
    GA for Set Covering Problem
    '''
    
    def __init__(self, problem):
        '''
        @param problem: problem
        @param nodes: list of nodes
        '''
        self.toolbox = base.Toolbox()
        creator.create("FitnessMin1", base.Fitness, weights=(-1.0,))
        creator.create("Individual1", array.array, typecode='i', fitness=creator.FitnessMin1, giant_tour=list, tours=list)
        
        current_gen = 0
        self.problem = problem
        
        self.POPSIZE=20
        self.NUMGEN=5
        self.INDSIZE = self.problem.num_of_nodes-1
        self.cxP=0.6
        self.mutP=1.0/self.INDSIZE
        
        self.initialize()
        
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
        
        
        
    def pop_init(self):
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
        
        binary_ind = [0]*self.INDSIZE
        for i in ind:
            binary_ind[i-1]=1
        return binary_ind
        
    
    def initialize(self):
        
#         self.toolbox.register("indices", self.pop_init)
        
        self.toolbox.register("indices", self.pop_gcsp_init)
        
        
        # Structure initializers
        self.toolbox.register("individual", tools.initIterate, creator.Individual1, self.toolbox.indices)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("mate", scpOnePointCX)#PMX)
#         tools.cxPartialyMatched(ind1, ind2)
#         self.toolbox.register("ls", mutLSVRP, problem=problem)
#         self.toolbox.register("ls4", mutLS4, problem=problem)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=self.mutP)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", self.eval)
                                    
    # evaluate solution
    def eval(self, individual):
        nodes = [i+1 for i in xrange(self.INDSIZE) if individual[i]==1]
        
        vrp_solver = GA_VRP(self.problem, nodes)
        cost, tours = vrp_solver.run()
                            
        individual.giant_tour=nodes
        individual.tours = tours
        
        return cost,
    
    def repair_ind(self, ind):
        w=[0]*self.problem.num_of_customers
        
        S = ind.giant_tour
        
        for i in xrange(self.problem.num_of_customers):
            w[i] = len(set(ind.giant_tour).intersection(self.problem.nodes_covering_customer[i]))
            
        U=[i for i in xrange(self.problem.num_of_customers) if w[i]==0]
        
        for i in U:
            # get nodes that cover customer i
            nodes = self.problem.nodes_covering_customer[i]
            # randomly select one
            j = random.choice(tuple(nodes))
            for t in self.problem.get_set_of_customers_covered_by(j):
                w[t] += 1
                
            S.append(j)
        
        # remove redundant node
        S = sorted(S)
        
        for j in S:
            temp = True
            for i in self.problem.get_set_of_customers_covered_by(j):
                if w[i] < 2:
                    temp = False
                    break
            if temp:
                S.remove(j)
#                 print j
                for i in self.problem.get_set_of_customers_covered_by(j):
                    w[i] = w[i]-1
            
        new_ind=self.toolbox.clone(ind)    
        for i in xrange(self.INDSIZE):
            new_ind[i]=0
            
        for i in S:
            new_ind[i-1]=1
            
        return new_ind
        
        
        
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
            offspring = varAndSCP(offspring, self.toolbox, cxpb, mutpb, gen)
            
            # repairing
            for i in xrange(len(offspring)):
                offspring[i]=self.repair_ind(offspring[i])
            
            
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
    
            print halloffame[0].tours
            
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
               toolbox=self.toolbox, cxpb=self.cxP, mutpb=1.0, 
               ngen=NUM_GEN, stats=stats, halloffame=hof, verbose=VERBOSE)
        
        print 'run ', job, ': ', hof[0].fitness.values[0], ': ', problem.best_cost, ': ', problem.n_same_giant_tour
    
    #     print hof[0].giant_tour
    #     print hof[0].tours
    #     calculate_tours_cost(problem, hof[0].tours, job)
    
        return hof[0]

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
        ga = GA_SCP(problem)
        ga.run(0)
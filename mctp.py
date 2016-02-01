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

from problem import CTPProblem, MCTPProblem, GMCTPProblem
from os.path import join

from setting import *
from deap.algorithms import varAnd
from crossovers import PMX, vrpPMX, scpOnePointCX
from genetic import varAndLS, varAndVRP, varAndSCP
from mutations import *
from datetime import timedelta
# from ga_vrp import GA_VRP
from hoang import ELS
from copy import deepcopy
from ls_moves import *
from ls import LS4


class GA_MCTP:
    '''
    GA for CTP with individual = giant tour
    '''
    
    def __init__(self, problem, job):
        '''
        @param problem: problem
        @param nodes: list of nodes
        '''
        self.job = job
        random.seed(1000+job)

        self.toolbox = base.Toolbox()
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin, tours=list)
        
        current_gen = 0
        self.problem = problem
        
        self.INDSIZE = self.problem.num_of_nodes + len(self.problem.obligatory_nodes)
        
        self.init_popsize=0
        
        self.initialize(problem.name)
        
        # for testing only
        self.best_cost = 10**10
        # job, gen
        self.stats = []
        
        self.sharking=False
        self.num_sharking_redundant_nodes = 0
        self.num_of_sharking = 0
        
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
    
    def LS_initialInd(self, giant_tour):
        if random.random() > 0.1:
            return giant_tour
        
        cost, backtrack = self.problem.split(giant_tour)
        
        # if infeasible giant tour
        if cost == MAX_VALUE:
            return None
         
        tours = problem.extract_tours(giant_tour, backtrack)
        old_cost = cost 
        
        new_giant_tour, new_tours, new_cost = LSPrins(problem, giant_tour, tours, old_cost)
        
        num_trails = 0
        while num_trails < MAX_TRAILS and new_cost < old_cost:
            num_trails += 1
            old_cost = new_cost
            new_giant_tour, new_tours, new_cost = LSPrins(problem, new_giant_tour, new_tours, new_cost)
                  
        return new_giant_tour
    
        
    def random_init(self):
        '''
        randomly initialize individuals
        '''
        size = self.problem.num_of_nodes + len(self.problem.obligatory_nodes)
        # khoi tao bang 1 diem ngau nhien
        sample_ind = random.sample(range(1, size+1), size)
        
        ind = []
        covering_set = set() #self.problem.get_set_of_customers_covered_by(ind[0])
        
        for node in sample_ind:
                       
            ind.append(node)
            covering_set.update(self.problem.get_set_of_customers_covered_by(node))
            
            if len(covering_set) == self.problem.num_of_customers:
                break
            
        
        ind = self.problem.remove_node(ind)

        # insert node in T
        nodes_set = set(ind)
        obligatory_nodes_not_in_giant_tour = self.problem.obligatory_nodes.difference(nodes_set)
        for node in list(obligatory_nodes_not_in_giant_tour):
            idx = random.randint(0, len(ind))
            ind.insert(idx, node)

        return self.LS_initialInd(ind) 
        
        
    def distance_init(self):
        '''
        select nodes base on distance
        '''
        ind_size = self.problem.num_of_nodes + len(self.problem.obligatory_nodes)
        # khoi tao bang 1 diem ngau nhien
        ind = [random.randint(1, ind_size)]
        ind_set = set(ind)
        covering_set = self.problem.get_set_of_customers_covered_by(ind[0])
        
        while len(covering_set) < self.problem.num_of_customers:
            
            # get the last node in ind
            node = ind[-1]
            
            # lay tap cac node sap xep theo khoang cach toi node
            distance_dict = problem.nodes[node].cost_dict
            
            sorted_distance = sorted(distance_dict.items(), key=operator.itemgetter(1))
            
            valid_neighbors=[]
            for neighbor_node, cost in sorted_distance:
                if neighbor_node!= 0 and not ind_set.issuperset(set([neighbor_node])):
                    valid_neighbors.append(neighbor_node)
                    
                if len(valid_neighbors) == MAX_NEIGHBORS:
                    break
            # pick one node from valid neighbor nodes
            next_node = random.sample(valid_neighbors, 1)[0]
            
            # update ind and ind_set
            ind.append(next_node)
            ind_set.add(next_node)
            covering_set.update(self.problem.get_set_of_customers_covered_by(next_node))
            
        
        ind = self.problem.remove_node(ind)

        # insert node in T
        nodes_set = set(ind)
        obligatory_nodes_not_in_giant_tour = self.problem.obligatory_nodes.difference(nodes_set)
        for node in list(obligatory_nodes_not_in_giant_tour):
            idx = random.randint(0, len(ind))
            ind.insert(idx, node)

        return self.LS_initialInd(ind) 
        
    def ind_init(self):
        '''
        khoi tao individuals = hoan vi cua cac node trong nodes
        '''            
        # get nodes with distance from depot to it is less than max_tour_length
#         candidate_nodes = [node for node in range(1, self.problem.num_of_nodes) \
#                            if self.problem.nodes[0].cost_dict[node] * 2 <= self.problem.max_tour_length]
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
#         return self.LS_initialInd(ind)
        
    def ind_init_gmctp(self):
        '''
        khoi tao individuals = hoan vi cua cac node trong nodes
        '''            
        # get nodes with distance from depot to it is less than max_tour_length
#         candidate_nodes = [node for node in range(1, self.problem.num_of_nodes) \
#                            if self.problem.nodes[0].cost_dict[node] * 2 <= self.problem.max_tour_length]
        ind=[]
        # w[i]=the number of columms that cover row i
        w=[0]*self.problem.num_of_customers
        for c in xrange(self.problem.num_of_customers):
            if w[c] >= self.problem.customer_covering[c]:
                continue
            # randomly select k nodes that covers customer c
            covered_nodes = self.problem.nodes_covering_customer[c]
            candidate_nodes = covered_nodes.difference(set(ind))
            
            k = self.problem.customer_covering[c]-w[c]
            
            nodes = random.sample(candidate_nodes, k)
            ind = ind + nodes
            for node in nodes:
                for i in self.problem.get_set_of_customers_covered_by(node):
                    w[i]+=1
            
        # remove redundant node
        T = ind[:]
        while len(T) > 0:
            j = random.choice(T)
            T.remove(j)
            temp=True
            for c in self.problem.get_set_of_customers_covered_by(j):
                if w[c]<= self.problem.customer_covering[c]:
                    temp=False
                    break
            if temp:
                ind.remove(j)
                for c in self.problem.get_set_of_customers_covered_by(j):
                    w[c] = w[c]-1
        
                    
        for i in xrange(len(self.problem.obligatory_nodes)):
            index = random.randint(0, len(ind)-1)
            ind.insert(index, i+1)
            
        return ind
#         return self.LS_initialInd(ind)
    
    def init_mip(self):
        '''
        Khoi tao SCP tu MIP
        '''
        nodes = self.lines[2*self.init_popsize+1].split()
        nodes = [int(v) for v in nodes]
        
        return nodes
        
    def hybird_init(self):
        if random.random() < 0.2:
            return self.random_init()
        else:
            return self.ind_init()
        
    def initialize(self, problem_name):
        
        self.toolbox.register("indices", self.ind_init_gmctp)
#         self.toolbox.register("indices", self.random_init)
        
#         self.toolbox.register("indices", self.hybird_init)
        
#         self.toolbox.register("indices", self.init_mip)
        
        
        # Structure initializers
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.indices)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
#         self.toolbox.register("mate", tools.cxUniform, indpb=INDPB)
        self.toolbox.register('mate', tools.cxTwoPoint)
#         tools.cxPartialyMatched(ind1, ind2)
#         self.toolbox.register("ls", mutLSVRP, problem=problem)
        self.toolbox.register("mutateLSPrins", mutLSPrins, problem=self.problem, max_trails=MAX_TRAILS)
        self.toolbox.register("mutate", mutShaking, problem=self.problem, k=3)
#        self.toolbox.register("mutate", new_mutation, problem=self.problem, remove_prob=REMOVE_PROB)        
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", self.eval)
        
#         mip_data_dir = 'SubSet'
#         self.lines = open(join(mip_data_dir, problem_name),'r').readlines()

                                    
    # evaluate solution
    def eval(self, individual):
        giant_tour = [node for node in individual]
                
#         print giant_tour
#         if not individual.fitness.valid:
        cost, backtrack = self.problem.split(giant_tour)
#         individual.fitness.values = cost,
        individual.tours = self.problem.extract_tours(giant_tour, backtrack)
                                
        return cost,
    
#         new_giant_tour, new_tours, new_cost = ELS(self.problem, giant_tour, individual.tours, individual.fitness.values[0])

            
#         return new_cost,
    
    def repair_ind(self, ind):
        '''
        chon node de tao loi giai phu nhieu nhat
        '''
        giant_tour = [i for i in ind]
        
        # remove dupblicate node in giant tour
        nodes_set = set(giant_tour)
        if len(nodes_set) < len(giant_tour):
            new_giant_tour = []
            for node in giant_tour:
                if nodes_set.issuperset(set([node])):
                    new_giant_tour.append(node)
                    nodes_set.discard(node)
            
            giant_tour = new_giant_tour
            
#         print giant_tour
        
        if not self.problem.is_giant_tour_satisfy_covering_constraint(giant_tour):
            # try until find feasible giant tour
            while True:
                nodes_in_giant_tour = set(giant_tour)
                nodes_not_in_giant_tour = set(range(1, len(self.problem.nodes))).difference(nodes_in_giant_tour)
                
                nodes_not_in_giant_tour = list(nodes_not_in_giant_tour)
                
                covering_set = self.problem.get_set_of_customers_covered_by_giant_tour(giant_tour)
                
                max_node = nodes_not_in_giant_tour[0]
                new_covering_set = covering_set.union(self.problem.get_set_of_customers_covered_by(max_node))
                max_covered = len(new_covering_set)
                for node in nodes_not_in_giant_tour[1:]:
                    new_covering_set = covering_set.union(self.problem.get_set_of_customers_covered_by(node))
                    if len(new_covering_set) > max_covered:
                        max_covered = len(new_covering_set)
                        max_node = node
                        
                # insert max_node into giant tour at random position
                idx = random.randint(0, len(giant_tour))
                giant_tour.insert(idx, max_node)
                
                # if is feasible giant tour then break while loop
                if self.problem.is_giant_tour_satisfy_covering_constraint(giant_tour):
                    break
#         print giant_tour
        # remove redundent nodes
        old_len = len(giant_tour)
        giant_tour = self.problem.remove_node(giant_tour)
        
        if self.sharking:
            self.num_sharking_redundant_nodes += old_len - len(giant_tour)
        # insert nodes in T
        nodes_set = set(giant_tour)
        self.problem.obligatory_nodes
        obligatory_nodes_not_in_giant_tour = self.problem.obligatory_nodes.difference(nodes_set)
        for node in list(obligatory_nodes_not_in_giant_tour):
            idx = random.randint(0, len(giant_tour))
            giant_tour.insert(idx, node)
            
        # update individual
        new_ind = deepcopy(ind)
        
        del new_ind[:]
        for node in giant_tour:
            new_ind.append(node)
        
        cost, backtrack = self.problem.split(giant_tour)
#         new_ind.fitness.values = cost,
        new_ind.tours = self.problem.extract_tours(giant_tour, backtrack)
        
        new_ind.fitness.values = cost,
        
        return new_ind

    def repair_ind_rnd(self, ind):
        '''
        chon node ngau nhien
        '''
                
        giant_tour = [i for i in ind]
        
        # remove dupblicate node in giant tour
        nodes_set = set(giant_tour)
        if len(nodes_set) < len(giant_tour):
            new_giant_tour = []
            for node in giant_tour:
                if nodes_set.issuperset(set([node])):
                    new_giant_tour.append(node)
                    nodes_set.discard(node)
            
            giant_tour = new_giant_tour
            
#         print giant_tour
        nodes_in_giant_tour = set(giant_tour)
        nodes_not_in_giant_tour = set(range(1, len(self.problem.nodes))).difference(nodes_in_giant_tour)
                
        nodes_not_in_giant_tour = list(nodes_not_in_giant_tour)
                        
        while not self.problem.is_giant_tour_satisfy_covering_constraint(giant_tour):
            # randomly choice a node                
            rnd_node = random.choice(nodes_not_in_giant_tour)

            # insert max_node into giant tour at random position
            idx = random.randint(0, len(giant_tour))
            giant_tour.insert(idx, rnd_node)
            
            # update
            nodes_not_in_giant_tour.remove(rnd_node)

#         print giant_tour

        # remove redundent nodes
        old_len = len(giant_tour)
        giant_tour = self.problem.remove_node(giant_tour)
        
        if self.sharking:
            self.num_sharking_redundant_nodes += old_len - len(giant_tour)
        # insert nodes in T
        nodes_set = set(giant_tour)
        self.problem.obligatory_nodes
        obligatory_nodes_not_in_giant_tour = self.problem.obligatory_nodes.difference(nodes_set)
        for node in list(obligatory_nodes_not_in_giant_tour):
            idx = random.randint(0, len(giant_tour))
            giant_tour.insert(idx, node)
            
        # update individual
        new_ind = deepcopy(ind)
        
        del new_ind[:]
        for node in giant_tour:
            new_ind.append(node)
        
        cost, backtrack = self.problem.split(giant_tour)
#         new_ind.fitness.values = cost,
        new_ind.tours = self.problem.extract_tours(giant_tour, backtrack)
        
        new_ind.fitness.values = cost,
        
        return new_ind

        
    def repair_ind_rnd_gmctp(self, individual):
        '''
        adap from init_ind
        
        khoi tao individuals = hoan vi cua cac node trong nodes
        '''            
        ind = [node for node in individual]
        nodes_set = set(ind)
        if len(nodes_set) < len(ind):
            new_giant_tour = []
            for node in ind:
                if nodes_set.issuperset(set([node])):
                    new_giant_tour.append(node)
                    nodes_set.discard(node)
            
            ind = new_giant_tour

#         print 'before repair: ', ind
        # w[i]=the number of columms that cover row i
        w=[0]*self.problem.num_of_customers
        
        for node in ind:
            for c in self.problem.get_set_of_customers_covered_by(node):
                w[c] += 1
                
        for c in xrange(self.problem.num_of_customers):
            if w[c] >= self.problem.customer_covering[c]:
                continue
            # randomly select k nodes that covers customer c
            covered_nodes = self.problem.nodes_covering_customer[c]
            # accept nodes that not in ind
            candidate_nodes = covered_nodes.difference(set(ind))
            
            k = self.problem.customer_covering[c]-w[c]
            
            nodes = random.sample(candidate_nodes, k)
            for node in nodes:
                idx = random.randint(0, len(ind)-1)
                ind.insert(idx, node)

            for node in nodes:
                for i in self.problem.get_set_of_customers_covered_by(node):
                    w[i]+=1
            
        # remove redundant node
        T = ind[:]
        while len(T) > 0:
            j = random.choice(T)
            T.remove(j)
            temp=True
            for c in self.problem.get_set_of_customers_covered_by(j):
                if w[c]<= self.problem.customer_covering[c]:
                    temp=False
                    break
            if temp:
                ind.remove(j)
                for c in self.problem.get_set_of_customers_covered_by(j):
                    w[c] = w[c]-1
        
                    
        for i in xrange(len(self.problem.obligatory_nodes)):
            index = random.randint(0, len(ind)-1)
            ind.insert(index, i+1)
            
        # update individual
        new_ind = deepcopy(individual)
        
        del new_ind[:]
        for node in ind:
            new_ind.append(node)
        
#         print 'after repair: ', ind
        
        cost, backtrack = self.problem.split(ind)
#         new_ind.fitness.values = cost,
        new_ind.tours = self.problem.extract_tours(ind, backtrack)
        
        new_ind.fitness.values = cost,
        
        return new_ind
#         return self.LS_initialInd(ind)

    def varAndPTA(self, population):
        self.sharking=False       

#         for i in range(len(population)):
#             if random.random() < PLSPRINS:
#                 population[i] = self.toolbox.mutateLSPrins(population[i])
        
        selected_pop = self.toolbox.select(population, len(population))
        offspring = [self.toolbox.clone(ind) for ind in selected_pop]
#                 
        # Apply crossover and mutation on the offspring
        for i in range(1, len(offspring), 2):
            if random.random() < PCROSS:
                offspring[i-1], offspring[i] = self.toolbox.mate(offspring[i-1], offspring[i])
                del offspring[i-1].fitness.values, offspring[i].fitness.values
                 
                # repair
#                 offspring[i-1] = self.repair_ind(offspring[i-1])
                offspring[i-1] = self.repair_ind_rnd(offspring[i-1])
                if random.random() < CROSS_PRINS_PROB:
                    offspring[i-1] = self.toolbox.mutateLSPrins(offspring[i-1])

#                 offspring[i] = self.repair_ind(offspring[i])
                offspring[i] = self.repair_ind_rnd(offspring[i])
                if random.random() < CROSS_PRINS_PROB:
                    offspring[i] = self.toolbox.mutateLSPrins(offspring[i])

#         
        for i in range(len(offspring)):#             
            if random.random() < PMUTATION:
                offspring[i] = self.toolbox.mutate(offspring[i])
                 
                del offspring[i].fitness.values
                self.num_of_sharking += 1
                self.sharking=True
#                 offspring[i] = self.repair_ind(offspring[i])
                offspring[i] = self.repair_ind_rnd(offspring[i])
                
                if random.random() < MUT_PRINS_PROB:
                    offspring[i] = self.toolbox.mutateLSPrins(offspring[i])

                self.sharking=False        
            
        return offspring
            
        
    def evolve(self, population, toolbox, cxpb, mutpb, ngen, stats=None, sizeStats=None,
                 halloffame=None, verbose=__debug__):
        global current_gen
        
        logbook = tools.Logbook()
        logbook.header = ['gen', 'best_of_gen', 'nevals'] + (stats.fields if stats else [])
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
    
        if halloffame is not None:
            halloffame.update(population)
    
        record = stats.compile(population) if stats else {}
#         record.update(sizeStats.compile(population) if sizeStats else {})
        best_cost = halloffame[0].fitness.values[0]
        best_tours = halloffame[0].tours
        best_giant_tour = [node for node in halloffame[0]]
        
        logbook.record(gen=0, best_of_gen=best_cost, nevals=len(invalid_ind),**record)
        
        if verbose:
            print logbook.stream
        
        num_gen_no_improve = 0
        # Begin the generational process
        for gen in range(1, ngen+1):
            current_gen = gen
            # Select the next generation individuals
#             offspring = toolbox.select(population, len(population))
            
            # Vary the pool of individuals
            offspring = self.varAndPTA(population)
                        
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
                            
            # Replace the current population by the offspring
            population[:] = offspring

             # elitism k best individuals
             
            idxs = random.sample(range(len(population)),len(halloffame))
            for idx, ind in zip(idxs, halloffame):
                population[idx]=ind
            
            # Update the hall of fame with the generated individuals
            if halloffame is not None:
                old_best_fitness = halloffame[0].fitness.values[0]

                halloffame.update(population)
                
                new_best_fitness = halloffame[0].fitness.values[0]
            
                if old_best_fitness == new_best_fitness:
                    num_gen_no_improve += 1
                else:
                    num_gen_no_improve = 0
                    
            if num_gen_no_improve == MAX_NUM_GEN_NO_IMPROVE:
                break

            # Append the current generation statistics to the logbook
            record = stats.compile(population) if stats else {}
#             record.update(sizeStats.compile(population) if sizeStats else {})
            
            logbook.record(gen=gen, best_of_gen=halloffame[0].fitness.values[0], nevals=len(invalid_ind), **record)
            if verbose:
                print logbook.stream        
    
#         return best_cost, best_tours
        return halloffame[0].fitness.values[0], halloffame[0].tours
    
    
    def run(self):
#        print self.problem.name
#         POPSIZE= 200 #len(self.lines)/2
        popsize = POPSIZE
        ngen = NUM_GEN
#         ngen = 20
#         T = len(self.problem.obligatory_nodes)+1
#         
#         if T == 10:
#             ngen = 50
#         elif T == 20:
#             ngen = 100
            
        pop = self.toolbox.population(n=popsize)
        
#         for i in xrange(popsize):
#             print i, pop[i]
    
        hof = tools.HallOfFame(2)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        
#         sizeStats = tools.Statistics(lambda ind: len(ind.giant_tour))
#         sizeStats.register('size_avg', numpy.mean)
        
        best_cost, best_tours = self.evolve(population=pop, 
               toolbox=self.toolbox, cxpb=PCROSS, mutpb=PMUTATION, 
               ngen=ngen, stats=stats, halloffame=hof, verbose=VERBOSE)
        
#         print 'run ', job, ': ', hof[0].fitness.values[0], ': ', problem.best_cost, ': ', problem.n_same_giant_tour
        print 'run %d: %.2f %d %d' %(self.job, best_cost, self.num_sharking_redundant_nodes, self.num_of_sharking)
    #     print hof[0].giant_tour
    #     print hof[0].tours
    #     calculate_tours_cost(problem, hof[0].tours, job)
    
        return best_cost , best_tours

import glob, os, datetime
if __name__ == "__main__":
    # load problem
    data_dir = 'data_mctp1/' # + folder + '/'
    print data_dir
#     Jobs = 10
    
    lines = []
    
    files = [
             
#             os.path.join(data_dir, 'A1-1-25-75-4.ctp'),
#             os.path.join(data_dir, 'A1-1-25-75-5.ctp'),
#             os.path.join(data_dir, 'A1-1-25-75-6.ctp'),
#             os.path.join(data_dir, 'D1-10-50-50-6.ctp'),
#  
#             os.path.join(data_dir, 'A2-20-100-100-4.ctp'),
#             os.path.join(data_dir, 'A2-20-100-100-5.ctp'),

#            os.path.join(data_dir, 'A2-10-50-150-4-250.ctp'),
            os.path.join(data_dir, 'A2-1-100-100-4-250.ctp'),
#             os.path.join(data_dir, 'B2-1-50-150-5-250.ctp'),
#             os.path.join(data_dir, 'B2-1-50-150-5-500.ctp'),
            
            
#             os.path.join(data_dir, 'B2-10-50-150-6-250.ctp'),
#             os.path.join(data_dir, 'B2-10-50-150-8.ctp'),
            ]
#     files = [os.path.join(data_dir, 'A-50-50-6.ctp')]
#     files = glob.glob(data_dir + '*.ctp')

    moves_freq = {}
#     lengths = [250,500,250,500]
#     lengths = [250]
    ro = 500
    
    for file in files:
        time1 = datetime.datetime.now()
        file_name = os.path.basename(file)
        print file_name, 
        
        # convert gmctp visit moi node nhieu lan sang visit moi node 1 lan
#         problem = GMCTPProblem(data_path=file)        
#         problem.convert_to_gmctp1()
        
        # generate gmctp problem
        problem = MCTPProblem(data_path=file)
        problem.export_gmctp()
        
        # export gmctp voi rang buoc do dai moi route
#         n = problem.num_of_nodes + len(problem.obligatory_nodes) + 1
#         
#         cost_from_depot = [problem.nodes[0].cost_dict[node] for node in range(1, n)]
#         max_cost_from_depot = max(cost_from_depot)
#          
#         problem.max_tour_length = 2*max_cost_from_depot + ro
#         problem.max_nodes_per_route = 1000
#         
#         print problem.max_tour_length
#         problem = gcsp.GCSPProblem(data_path=file)
        
#         problem.export_gmctp(ro)
        
        # calculate solution cost
#         tours = [[46, 74, 27, 4, 94, 34, 79]]#, 
#         tours = [[13, 47, 36, 52]]
        tours = [[13, 47, 36, 52], [46, 74, 27, 4, 94, 34, 79]]
        cost = problem.get_solution_cost(tours)
        print cost
        print problem.is_tours_satisfy_covering_constraint(tours)
        break


#         best_solution = None
#         best_cost = MAX_VALUE
#           
#         best_runs =[]
#          
#         for job in xrange(JOBS):
#             ga = GA_MCTP(problem, job)
#             cost, tours = ga.run()
#              
#             best_runs.append(cost)
#               
#             if cost < best_cost:
#                 best_cost = cost
#                 best_solution = deepcopy(tours)
#                   
#         lines.append('%s %.2f %.2f %d [%s] %s\n' %(file_name, 
#                                                  problem.best_cost,
#                                                  best_cost, 
#                                                  len(best_solution),
# #                                                  d.seconds, 
#                                                  ' '.join([str(v) for v in best_runs]),
#                                                  str(best_solution),
# #                                                  str(best_solution.tours)
#                                                  ))
#   
# #         print best_cost, best_solution
#           
#     f = open('out/mctp.out', 'w')
#     f.writelines(lines)

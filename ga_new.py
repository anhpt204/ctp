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
from util import split, get_all_solutions, get_giant_tour, extract_tours,\
    calculate_tours_cost
from os.path import join

from setting import *
from deap.algorithms import varAnd
from crossovers import PMX
from genetic import varAndLS
from mutations import mutLS, mutLS4


# load problem
# data_path = '/home/pta/projects/ctp/data_ctp/kroA-13-12-75-4.ctp'
# problem = CTPProblem()
# problem.load_data(data_path)
toolbox = base.Toolbox()
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin, giant_tour=list, tours=list)

# giant_tour_cost = {}
# n_same_giant_tour = 0
current_gen = 0

def pop_init(problem, k=3):
    '''
    khoi tao individual bang cach chon 1 trong k diem (chua co trong) gan no nhat
    '''
    ind_size = problem.num_of_nodes + len(problem.obligatory_nodes) - 1
    # khoi tao bang 1 diem ngau nhien
    ind = [random.randint(1, ind_size)]
    ind_set = set(ind)
    
    while len(ind) < ind_size:
        
        # get the last node in ind
        node = ind[-1]
        
        # lay tap cac node sap xep theo khoang cach toi node
        distance_dict = problem.nodes[node].cost_dict
        
        sorted_distance = sorted(distance_dict.items(), key=operator.itemgetter(1))
        
        valid_neighbors=[]
        for neighbor_node, cost in sorted_distance:
            if neighbor_node!= 0 and not ind_set.issuperset(set([neighbor_node])):
                valid_neighbors.append(neighbor_node)
                
            if len(valid_neighbors) == k:
                break
        # pick one node from valid neighbor nodes
        next_node = random.sample(valid_neighbors, 1)[0]
        
        # update ind and ind_set
        ind.append(next_node)
        ind_set.add(next_node)
        
    return ind

def initialize(problem):
    # Attribute generator
    IND_SIZE = problem.num_of_nodes + len(problem.obligatory_nodes) -1
#     toolbox.register("indices", random.sample, range(1,IND_SIZE+1), IND_SIZE)
    toolbox.register("indices", pop_init,problem=problem, k=3)
    
    
    
    # Structure initializers
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", PMX)#PMX)
    toolbox.register("ls", mutLS, problem=problem)
    toolbox.register("ls4", mutLS4, problem=problem)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=INDPB)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", eval, problem=problem)
    
                    
def get_giant_tours(problem, individual):
    '''
    get giant tours of an individual
    try MAX_TRAILS times
    '''
    giant_tours =[]
#     MAX_TRAILS = 20
    for start_i in xrange(MAX_TRAILS):
        # get tour
        covering_set = set()
        tour = []
        
        # append nodes before start_i that in T into tour
        for node_id in individual[:start_i]:
            if problem.obligatory_nodes.issuperset(set([node_id])):
                tour.append(node_id)

        i = start_i
        while True:
            # infeasible
            if i >= len(individual):
                return giant_tours
            
            node_id = individual[i]
            i+=1
            # check if node belong to obligatory nodes
            if problem.obligatory_nodes.issuperset(set([node_id])):
                tour.append(node_id)
                continue
            
            covered_customers = problem.get_set_of_customers_covered_by(node_id)
            
            if covered_customers.issubset(covering_set):
                continue
            
            # update tour
            tour.append(node_id)
            
            # update covering set
            covering_set = covering_set.union(covered_customers)
            
            if len(covering_set) == problem.num_of_customers:
                break
            
            
            
        # append all remaining nodes in individual that also in obligatory nodes into tour
        for node_id in individual[i:]:
            if problem.obligatory_nodes.issuperset(set([node_id])):
                tour.append(node_id)

        giant_tours.append(tour)
        
    return giant_tours
# evaluate solution
def eval(individual, problem):
    global n_same_giant_tour
    
    best_cost = 10**10
    best_tour = None
    best_backtrack=None
    # get giant tours of an individual
#     giant_tours = get_giant_tours(individual)
#     giant_tours = get_all_solutions(problem, individual, current_gen)
    giant_tour = get_giant_tour(problem, individual)
    giant_tours = [giant_tour] # :D
    # get the best giant tour
    for giant_tour in giant_tours:    
#         print giant_tour
        key = tuple(giant_tour)
        cost = None
        backtrack=None
        
        if problem.giant_tour_cost.has_key(key):
            problem.n_same_giant_tour += 1
            cost,backtrack = problem.giant_tour_cost[key]
        else:
            cost, backtrack = split(problem, giant_tour)
            problem.giant_tour_cost[key] =  (cost, backtrack)
            
        if cost < best_cost:
            best_cost = cost
            best_tour = giant_tour[:]
            best_backtrack = backtrack[:]

    # split tour and return total cost
    individual.giant_tour = best_tour[:]
    individual.tours = extract_tours(best_tour, best_backtrack)
        
    return best_cost,


def evolve(problem, population, toolbox, cxpb, mutpb, ngen, stats=None, sizeStats=None,
             halloffame=None, verbose=__debug__):
    global current_gen
    
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else []) + (sizeStats.fields if sizeStats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    record.update(sizeStats.compile(population) if sizeStats else {})
    
    logbook.record(gen=0, nevals=len(invalid_ind),**record)
    
    if verbose:
        print logbook.stream
    
    num_ls = [[0,0]]
    # Begin the generational process
    for gen in range(1, ngen+1):
        num_ls.append([0,0])
        current_gen = gen
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))
        
        # Vary the pool of individuals
        offspring = varAndLS(offspring, toolbox, cxpb, mutpb, num_ls, gen)
        
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
        record.update(sizeStats.compile(population) if sizeStats else {})
        
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print logbook.stream        

    return population, logbook


def run(problem, job=0):
    random.seed(1000+job)

    pop = toolbox.population(n=POPSIZE)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    sizeStats = tools.Statistics(lambda ind: len(ind.giant_tour))
    sizeStats.register('size_avg', numpy.mean)
    
    evolve(problem=problem, population=pop, 
           toolbox=toolbox, cxpb=PCROSS, mutpb=PMUTATION, 
           ngen=NUM_GEN, stats=stats, sizeStats=sizeStats,halloffame=hof, verbose=VERBOSE)
    
    print 'run ', job, ': ', hof[0].fitness.values[0], ': ', problem.best_cost, ': ', problem.n_same_giant_tour

    print hof[0].giant_tour
    print hof[0].tours
    calculate_tours_cost(problem, hof[0].tours, job)
    return hof[0].fitness.values[0]

import glob, os, datetime
if __name__ == "__main__":
    # load problem
    folder = 'D'
    data_dir = 'data_ctp/' + folder + '/'
#     Jobs = 10
    
    files = glob.glob(data_dir + '*.ctp')
    lines = []
    
#     files = [os.path.join(data_dir, 'C1-13-25-75-4.ctp')]
#     files = [os.path.join(data_dir, 'A2-10-50-150-6.ctp')]
    
    
    for file in files:
        time1 = datetime.datetime.now()
        file_name = os.path.basename(file)
        print file_name
        
        problem = CTPProblem(data_path=file)
        
        initialize(problem=problem)
        
        best_x =[]
        
        for job in xrange(JOBS):
            
            best_cost = run(problem=problem, job=job)
            
            best_x.append(best_cost)
            
        time2 = datetime.datetime.now()
        
        lines.append( file_name + " " + str(min(best_x)) + " " + str(problem.best_cost) + " " + str(time2-time1) + '\n')

    open(folder+'.out', 'w').writelines(lines)

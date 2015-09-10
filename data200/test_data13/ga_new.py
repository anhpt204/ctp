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

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from problem import CTPProblem
from util import split
from os.path import join

# load problem
# data_path = '/home/pta/projects/ctp/data_ctp/kroA-13-12-75-4.ctp'
problem = CTPProblem()
# problem.load_data(data_path)
toolbox = base.Toolbox()
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin, giant_tour=list, tours=list)


def initialize():
    # ignore depot
    IND_SIZE = problem.num_of_nodes + len(problem.obligatory_nodes) -1



    # Attribute generator
    toolbox.register("indices", random.sample, range(1,IND_SIZE+1), IND_SIZE)
    
    # Structure initializers
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
                    
def get_giant_tours(individual):
    '''
    get giant tours of an individual
    try MAX_TRAILS times
    '''
    giant_tours =[]
    MAX_TRAILS = 20
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
def eval(individual):
    
    best_cost = 10**10
    best_tour = None
    # get giant tours of an individual
    giant_tours = get_giant_tours(individual)
    # get the best giant tour
    for giant_tour in giant_tours:    
        cost, backtrack = split(problem, giant_tour)
        if cost < best_cost:
            best_cost = cost
            best_tour = giant_tour[:]

    # split tour and return total cost
    individual.giant_tour = best_tour[:]
        
    return best_cost,

def PMX(ind1, ind2):
    """Executes a partially matched crossover (PMX) on the input individuals.
    The two individuals are modified in place. This crossover expects
    :term:`sequence` individuals of indices, the result for any other type of
    individuals is unpredictable.
    
    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.

    Moreover, this crossover generates two children by matching
    pairs of values in a certain range of the two parents and swapping the values
    of those indexes. For more details see [Goldberg1985]_.

    This function uses the :func:`~random.randint` function from the python base
    :mod:`random` module.
    
    .. [Goldberg1985] Goldberg and Lingel, "Alleles, loci, and the traveling
       salesman problem", 1985.
    """
    size = min(len(ind1), len(ind2))
    p1, p2 = [0]*(size+1), [0]*(size+1)

    # Initialize the position of each indices in the individuals
    for i in xrange(size):
        p1[ind1[i]] = i
        p2[ind2[i]] = i
    # Choose crossover points
    cxpoint1 = random.randint(0, size)
    cxpoint2 = random.randint(0, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else: # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1
    
    # Apply crossover between cx points
    for i in xrange(cxpoint1, cxpoint2):
        # Keep track of the selected values
        temp1 = ind1[i]
        temp2 = ind2[i]
        # Swap the matched value
        ind1[i], ind1[p1[temp2]] = temp2, temp1
        ind2[i], ind2[p2[temp1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]
    
    return ind1, ind2

toolbox.register("mate", PMX)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", eval)


def run(job=0):
    random.seed(1000+job)

    pop = toolbox.population(n=300)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    algorithms.eaSimple(pop, toolbox, 0.6, 0.4, 200, stats=stats, 
                        halloffame=hof, verbose=False)
    
    print 'run ', job, ': ', hof[0].fitness.values[0], ': ', problem.best_cost

    return hof[0].fitness.values[0]

import glob, os, datetime
if __name__ == "__main__":
    # load problem
    data_dir = '/home/pta/projects/ctp/test_data13/'
    Jobs = 10
    
    files = glob.glob(data_dir + '*.ctp')
    lines = []
    
#     files = [os.path.join(data_dir, 'kroB-1-99-100-4.ctp')]
    
    for file in files:
        time1 = datetime.datetime.now()
        file_name = os.path.basename(file)
        print file_name
        problem.load_data(file)
        initialize()
        
        best_x =[]
        for job in xrange(Jobs):
            best_cost = run(job)
            best_x.append(best_cost)
            
        time2 = datetime.datetime.now()
        
        lines.append( file_name + " " + str(min(best_x)) + " " + str(problem.best_cost) + " " + str(time2-time1) + '\n')

    open('result13.txt', 'w').writelines(lines)

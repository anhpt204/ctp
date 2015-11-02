'''
Created on Sep 8, 2015

@author: pta
'''
import random

from ls import ls_prins, ls_move14, ls_prins_vrp
from genetic import computeFitness
from ls_moves import move10

def mutShuffleIndexesCTP(individual, indpb):
    """Shuffle the attributes of the input individual and return the mutant.
    The *individual* is expected to be a :term:`sequence`. The *indpb* argument is the
    probability of each attribute to be moved. Usually this mutation is applied on 
    vector of indices.
    
    :param individual: Individual to be mutated.
    :param indpb: Independent probability for each attribute to be exchanged to
                  another position.
    :returns: A tuple of one individual.
    
    This function uses the :func:`~random.random` and :func:`~random.randint`
    functions from the python base :mod:`random` module.
    """
    size = len(individual)
    for i in xrange(size):
        if random.random() < indpb:
            swap_indx = random.randint(0, size - 2)
            if swap_indx >= i:
                swap_indx += 1
            individual[i], individual[swap_indx] = \
                individual[swap_indx], individual[i]
    
    return individual,


def mutLS(individual, problem, gen):
    """
    Local Search
    
    :param individual: Individual to be mutated.
    :param indpb: Independent probability for each attribute to be exchanged to
                  another position.
    :returns: A tuple of one individual.
    
    This function uses the :func:`~random.random` and :func:`~random.randint`
    functions from the python base :mod:`random` module.
    """
    if not individual.fitness.valid:
        computeFitness(problem, individual)
    
    individual = ls_prins(problem, individual, gen,)
#     individual = ls_move14(problem, individual, num_ls, gen)
    
    return individual,

def mutLSVRP(individual, problem, gen):
    """
    Local Search
    
    :param individual: Individual to be mutated.
    :param indpb: Independent probability for each attribute to be exchanged to
                  another position.
    :returns: A tuple of one individual.
    
    This function uses the :func:`~random.random` and :func:`~random.randint`
    functions from the python base :mod:`random` module.
    """
#     print 'in: ', individual
    if not individual.fitness.valid:
        cost, backtrack = problem.split(individual)
                
        # split tour and return total cost
        tour = [node for node in individual]
        individual.tours = problem.extract_tours(tour, backtrack)
        individual.fitness.values = cost, 
        
    
#     print individual
    individual = ls_prins_vrp(problem, individual, gen)

#     individual = ls_move14(problem, individual, num_ls, gen)
#     print 'out: ', individual
    
    return individual,

def mutLS4(individual, problem, num_ls, gen):
    if not individual.fitness.valid:
        computeFitness(problem, individual)
        
    num_ls[gen][0] += 1
    improvement, new_ind = move10(problem, individual)
    
    if improvement:
        num_ls[gen][1] += 1
        return new_ind,
    
    return individual,
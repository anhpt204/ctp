'''
Created on Sep 8, 2015

@author: pta
'''
from ls import ls_prins
from genetic import computeFitness
from ls_moves import move10

def mutLS(individual, problem, num_ls, gen):
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
    
    individual = ls_prins(problem, individual, num_ls, gen)
#     individual = ls_move14(individual, num_ls, gen)
    
    return individual,

def mutLS4(individual, problem, num_ls, gen):
    if not individual.fitness.valid:
        computeFitness(problem, individual)
        
    num_ls[gen][0] += 1
    ls4_improvement, new_ind = move10(problem, individual)
    
    if ls4_improvement:
        num_ls[gen][1] += 1
        return new_ind,
    
    return individual,
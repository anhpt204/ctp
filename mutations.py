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

def repair(problem, ind):
#     print 'in: ', ind
    # check if it contains all node in T
    ind_set = set(ind)
    # make sure each node appear only one time
    new_ind=[]
    if len(ind_set) < len(ind):
        node_dict={}
        for node in ind:
            if not node_dict.has_key(node):
                node_dict[node]=1
                new_ind.append(node)
        del ind[len(new_ind):]
        for i in xrange(len(ind)):
            ind[i] = new_ind[i]
        
    tmp = ind_set.intersection(problem.obligatory_nodes)
    if len(tmp) < len(problem.obligatory_nodes):
        ns = problem.obligatory_nodes.difference(tmp)
        for n in ns:
            ind.insert(random.randint(0, len(ind)), n)
            
    # check covering
    covering_set = set()
    for n in ind:
        if problem.obligatory_nodes.issuperset(set([n])):
            continue
        covering_set.update(problem.get_set_of_customers_covered_by(n))
        
    tmp = set(range(problem.num_of_customers))
    tmp = tmp.difference(covering_set)
    
    if len(tmp) == 0:
        return problem.remove_node(ind)
    
    # insert nodes to satisfy covering constraint
    ind_set = set(ind)
    out_nodes = set(range(1, len(problem.nodes)))
    out_nodes = out_nodes.difference(ind_set)
#     if out_nodes == None:
#         print 't'
    out_nodes = list(out_nodes)
    
    while len(covering_set) < problem.num_of_customers:
        best_node = out_nodes[0]
        best_covering_len = len(tmp.intersection(problem.get_set_of_customers_covered_by(best_node)))
        for node in out_nodes[1:]:
            covering_len = len(problem.get_set_of_customers_covered_by(node).intersection(tmp))
            if covering_len > best_covering_len:
                best_covering_len = covering_len
                best_node =  node
                
        covering_set.update(problem.get_set_of_customers_covered_by(best_node))
        
        ind.insert(random.randint(0, len(ind)), best_node)
        
        tmp = set(range(problem.num_of_customers))
        tmp = tmp.difference(covering_set)
        out_nodes.remove(best_node)
        
    return ind

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
#     if len(individual) != len(set(individual)):
#         print 'in: ', individual

    individual = repair(problem, individual)
    
    
    
    if not individual.fitness.valid:
        
        cost, backtrack = problem.split(individual)
                
        # split tour and return total cost
        tour = [node for node in individual]
        individual.tours = problem.extract_tours(tour, backtrack)
        individual.fitness.values = cost, 
        
#     print individual
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
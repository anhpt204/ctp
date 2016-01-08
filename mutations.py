'''
Created on Sep 8, 2015

@author: pta
'''
import random

from ls import ls_prins, ls_move14, ls_prins_vrp, LS3, LS2, LS1
from genetic import computeFitness
from ls_moves import move10, move10_vrp
from ga_gt import LSPrins

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
    '''
    repair an individual to become a feasible solution
    '''
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
#     individual = ls_prins_vrp(problem, individual, gen)
    for i in xrange(10):
        individual = LS1(problem, individual)
        individual = LS3(problem=problem, individual=individual)
        individual = LS2(problem=problem, individual=individual)
    
    ls4_improvement, individual = move10_vrp(problem, individual)
#     individual = ls_move14(problem, individual, num_ls, gen)
#     print 'out: ', individual
    
    new_giant_tour = problem.concat(individual.tours)
    del individual[len(new_giant_tour):]
    for i in xrange(len(individual)):
        individual[i]=new_giant_tour[i]

    
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

def mutShaking(individual, problem, k):
    '''
    remove k node
    '''
#     k = random.randint(2,4)
    candidate_removed_nodes = [node for node in individual if not problem.obligatory_nodes.issuperset(set([node]))]
    
    if k > len(candidate_removed_nodes):
        k = len(candidate_removed_nodes)/2
        
    removed_nodes = random.sample(candidate_removed_nodes, k)
    
    for node in removed_nodes:
        individual.remove(node)
        
    return individual

def new_mutation(individual, problem, remove_prob):
    '''
    remove k node
    '''
    k = random.randint(2,4)
    for node in individual:
        if random.random() < remove_prob:
            individual.remove(node)
                    
    return individual

def mutLSPrins(individual, problem, max_trails=12):
    
    giant_tour = [node for node in individual]
    
    if not individual.fitness.valid:
        return individual
    
    best_cost = individual.fitness.values[0]
    
    new_giant_tour, new_tours, new_cost = LSPrins(problem, giant_tour, individual.tours, best_cost)
    
    num_trails = 0
    while num_trails < max_trails and new_cost < best_cost:
        num_trails += 1
        best_cost = new_cost
        new_giant_tour, new_tours, new_cost = LSPrins(problem, new_giant_tour, new_tours, best_cost)
              
    
#         if new_cost < self.best_cost:
#             self.best_cost = new_cost
#         print new_cost, self.best_cost
        
    # re construct individual
    individual.tours = new_tours
        
    N = len(new_giant_tour)
    if N < len(individual):
        del individual[len(new_giant_tour):]
            
    assert len(individual)==N, 'len individual is not equal N'
    for i in xrange(N):
        individual[i]=new_giant_tour[i]
            
    individual.fitness.values = best_cost,
    
    return individual

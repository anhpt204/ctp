'''
Created on Aug 24, 2015

@author: pta
'''
from math import fabs
from copy import deepcopy
import random

def validate_tour(tour, value):
    while True:
        try:
            tour.remove(value)
        except:
            break
    if len(tour) == 0:
        return None
    else:
        return tour
        
def move1(individual, tour_i, tour_j, i, j, u, v, x, y):
    '''
    move 1: if u is a client node, move u after v
    @param individual: individual for move opterator
    @param tour_i: index of a tour
    @param tour_j: index of a tour
    @param i: index of a node in @tour_i
    @param j: index of a node in @tour_j
    @param u: value at index i of @tour_i
    @param v: value a index j of @tour_j
    @param x: is the successor of u
    @param y: is the successor of v
    '''
    temp_tours = deepcopy(individual.tours)
    tour_i_tmp = [0] + temp_tours[tour_i] + [0]

    tour_j_tmp = [0] + temp_tours[tour_j] + [0]
    if tour_i == tour_j:
        tour_j_tmp = tour_i_tmp
        
    move_success = False
    
    if u != 0 and u != v:
        move_success = True
        
        tour_i_tmp.remove(u)

        k = tour_j_tmp.index(v)
        
        tour_j_tmp.insert(k+1, u)
    
    temp_tours[tour_i] = validate_tour(tour_i_tmp, 0)
    temp_tours[tour_j] = validate_tour(tour_j_tmp, 0)
    
    temp_tours = validate_tour(temp_tours, None)
    
    return move_success,temp_tours

def move2(individual, tour_i, tour_j, i, j, u, v, x, y):
    '''
    move 2: if u and x are client nodes, move (u,x) after v
    @param individual: individual for move opterator
    @param tour_i: index of a tour
    @param tour_j: index of a tour
    @param i: index of a node in @tour_i
    @param j: index of a node in @tour_j
    @param u: value at index i of @tour_i
    @param v: value a index j of @tour_j
    @param x: is the successor of u
    @param y: is the successor of v
    '''
    temp_tours = deepcopy(individual.tours)
    tour_i_tmp = [0] + temp_tours[tour_i] + [0]
    
    tour_j_tmp = [0] + temp_tours[tour_j] + [0]
    if tour_i == tour_j:
        tour_j_tmp = tour_i_tmp
        
    move_success = False
    
    if u != 0 and x != 0 and u != v and u != y and x!= v and x != y:
        move_success = True
        tour_i_tmp.remove(u)
        tour_i_tmp.remove(x)
        
        k = tour_j_tmp.index(v)
        
        tour_j_tmp.insert(k+1, x)
        tour_j_tmp.insert(k+1, u)
    
    temp_tours[tour_i] = validate_tour(tour_i_tmp, 0)
    temp_tours[tour_j] = validate_tour(tour_j_tmp, 0)
    
    temp_tours = validate_tour(temp_tours, None)

    return move_success, temp_tours

def move3(individual, tour_i, tour_j, i, j, u, v, x, y):
    '''
    move 3: if u and x are client nodes, move (x,u) after v
    @param individual: individual for move opterator
    @param tour_i: index of a tour
    @param tour_j: index of a tour
    @param i: index of a node in @tour_i
    @param j: index of a node in @tour_j
    @param u: value at index i of @tour_i
    @param v: value a index j of @tour_j
    @param x: is the successor of u
    @param y: is the successor of v
    '''
    temp_tours = deepcopy(individual.tours)
    tour_i_tmp = [0] + temp_tours[tour_i] + [0]
    
    tour_j_tmp = [0] + temp_tours[tour_j] + [0]
    if tour_i == tour_j:
        tour_j_tmp = tour_i_tmp
        
    move_success = False
    
    if u != 0 and x != 0 and u != v and u != y and x!= v and x != y:
        move_success = True
        tour_i_tmp.remove(u)
        tour_i_tmp.remove(x)
        
        k = tour_j_tmp.index(v)
        
        tour_j_tmp.insert(k+1, u)
        tour_j_tmp.insert(k+1, x)
    
    temp_tours[tour_i] = validate_tour(tour_i_tmp, 0)
    temp_tours[tour_j] = validate_tour(tour_j_tmp, 0)
    
    temp_tours = validate_tour(temp_tours, None)
    
    return move_success, temp_tours

def move4(individual, tour_i, tour_j, i, j, u, v, x, y):
    '''
    move 4: if u and v are client nodes, permute u and v
    @param individual: individual for move opterator
    @param tour_i: index of a tour
    @param tour_j: index of a tour
    @param i: index of a node in @tour_i
    @param j: index of a node in @tour_j
    @param u: value at index i of @tour_i
    @param v: value a index j of @tour_j
    @param x: is the successor of u
    @param y: is the successor of v
    '''
    temp_tours = deepcopy(individual.tours)
    tour_i_tmp = [0] + temp_tours[tour_i] + [0]

    tour_j_tmp = [0] + temp_tours[tour_j] + [0]
    if tour_i == tour_j:
        tour_j_tmp = tour_i_tmp
    
    move_success = False

    if u != 0 and v != 0 and u != v and u != y and x!= v and x != y:
        move_success = True
        tour_i_tmp[i] = v
        tour_j_tmp[j] = u

    temp_tours[tour_i] = validate_tour(tour_i_tmp,0)
    temp_tours[tour_j] = validate_tour(tour_j_tmp,0)
        
    temp_tours = validate_tour(temp_tours, None)

    return move_success, temp_tours

def move5(individual, tour_i, tour_j, i, j, u, v, x, y):
    '''
    move 5: if u, x and v are client nodes, permute (u,x) with v
    @param individual: individual for move opterator
    @param tour_i: index of a tour
    @param tour_j: index of a tour
    @param i: index of a node in @tour_i
    @param j: index of a node in @tour_j
    @param u: value at index i of @tour_i
    @param v: value a index j of @tour_j
    @param x: is the successor of u
    @param y: is the successor of v
    '''
    temp_tours = deepcopy(individual.tours)
    tour_i_tmp = [0] + temp_tours[tour_i] + [0]
    
    tour_j_tmp = [0] + temp_tours[tour_j] + [0]
    if tour_i == tour_j:
        tour_j_tmp = tour_i_tmp
        
    move_success = False

    if u != 0 and x != 0 and v != 0 and u != v and u != y and x!= v and x != y:
        move_success = True
        
        tour_j_tmp[j] = -1
        tour_i_tmp.remove(u)
        tour_i_tmp.remove(x)
        
        tour_i_tmp.insert(i, v)
        k = tour_j_tmp.index(-1)
        tour_j_tmp[k] = u
        tour_j_tmp.insert(k+1, x)

    temp_tours[tour_i] = validate_tour(tour_i_tmp,0)
    temp_tours[tour_j] = validate_tour(tour_j_tmp,0)
    
    temp_tours = validate_tour(temp_tours, None)

    return move_success, temp_tours

def move6(individual, tour_i, tour_j, i, j, u, v, x, y):
    '''
    move 6: if u,x and v,yf are client nodes, permute (u,x) with (v,y)
    @param individual: individual for move opterator
    @param tour_i: index of a tour
    @param tour_j: index of a tour
    @param i: index of a node in @tour_i
    @param j: index of a node in @tour_j
    @param u: value at index i of @tour_i
    @param v: value a index j of @tour_j
    @param x: is the successor of u
    @param y: is the successor of v
    '''
    temp_tours = deepcopy(individual.tours)
    tour_i_tmp = [0] + temp_tours[tour_i] + [0]
    
    tour_j_tmp = [0] + temp_tours[tour_j] + [0]
    if tour_i == tour_j:
        tour_j_tmp = tour_i_tmp

    move_success = False

    if u != 0 and x != 0 and v != 0 and y != 0 and u != v and u != y and x!= v and x != y:
        move_success = True
        tour_i_tmp[i] = v
        tour_i_tmp[i+1] = y
        
        tour_j_tmp[j] = u
        tour_j_tmp[j+1] = x

    temp_tours[tour_i] = validate_tour(tour_i_tmp,0)
    temp_tours[tour_j] = validate_tour(tour_j_tmp,0)

    temp_tours = validate_tour(temp_tours, None)

    return move_success, temp_tours

def move7(individual, tour_i, tour_j, i, j, u, v, x, y):
    '''
    move 7: if (u,x) and (v,y) are are non adjacent in the same trip, replace them by (u,v) and (x,y)
    @param individual: individual for move opterator
    @param tour_i: index of a tour
    @param tour_j: index of a tour
    @param i: index of a node in @tour_i
    @param j: index of a node in @tour_j
    @param u: value at index i of @tour_i
    @param v: value a index j of @tour_j
    @param x: is the successor of u
    @param y: is the successor of v
    '''
    temp_tours = deepcopy(individual.tours)
    tour_i_tmp = [0] + temp_tours[tour_i] + [0]
    tour_j_tmp = tour_i_tmp
    move_success = False

    if tour_i == tour_j and fabs(i-j) > 2 and u != v and u != y and x!= v and x != y:
        move_success = True
        tour_i_tmp[i+1] = v
        tour_j_tmp[j] = x

    temp_tours[tour_i] = validate_tour(tour_i_tmp,0)
    temp_tours[tour_j] = validate_tour(tour_j_tmp,0)
    
    temp_tours = validate_tour(temp_tours, None)
        
    return move_success, temp_tours

def move8(individual, tour_i, tour_j, i, j, u, v, x, y):
    '''
    move 8: if (u,x) and (v,y) are in distinct trips, replace them by (u,v) and (x,y)
    @param individual: individual for move opterator
    @param tour_i: index of a tour
    @param tour_j: index of a tour
    @param i: index of a node in @tour_i
    @param j: index of a node in @tour_j
    @param u: value at index i of @tour_i
    @param v: value a index j of @tour_j
    @param x: is the successor of u
    @param y: is the successor of v
    '''
    temp_tours = deepcopy(individual.tours)
    tour_i_tmp = [0] + temp_tours[tour_i] + [0]
    tour_j_tmp = [0] + temp_tours[tour_j] + [0]
    move_success = False
    if tour_i != tour_j:
        move_success = True
        tour_i_tmp[i+1] = v
        tour_j_tmp[j] = x
            
    temp_tours[tour_i] = validate_tour(tour_i_tmp,0)
    temp_tours[tour_j] = validate_tour(tour_j_tmp,0)

    temp_tours = validate_tour(temp_tours, None)    
    
    return move_success, temp_tours

def move9(individual, tour_i, tour_j, i, j, u, v, x, y):
    '''
    move 8: if (u,x) and (v,y) are in distinct trips, replace them by (u,y) and (x,v)
    @param individual: individual for move opterator
    @param tour_i: index of a tour
    @param tour_j: index of a tour
    @param i: index of a node in @tour_i
    @param j: index of a node in @tour_j
    @param u: value at index i of @tour_i
    @param v: value a index j of @tour_j
    @param x: is the successor of u
    @param y: is the successor of v
    '''
    temp_tours = deepcopy(individual.tours)
    tour_i_tmp = [0] + temp_tours[tour_i] + [0]
    tour_j_tmp = [0] + temp_tours[tour_j] + [0]
    move_success = False

    if tour_i != tour_j:
        move_success = True
        tour_i_tmp[i+1] = y
        
        tour_j_tmp[j] = x
        tour_j_tmp[j+1] = v
        
    temp_tours[tour_i] = validate_tour(tour_i_tmp,0)
    temp_tours[tour_j] = validate_tour(tour_j_tmp,0)
        
    temp_tours = validate_tour(temp_tours, None)

    return move_success, temp_tours

def move10(problem, individual):
    '''
    replace a node in a tour with another node outside of giant tour
    '''
    new_ind = deepcopy(individual)
    
    old_fitness = individual.fitness.values[0]
    
    # get all nodes that are not in tours
    nodes_in_tours = set(individual.giant_tour)
    nodes_not_in_tours = set(individual).difference(nodes_in_tours)

    # make a new tours
    new_tours = deepcopy(individual.tours[:])      
                
    for tour_idx in xrange(len(individual.tours)):
#         old_tour = individual.tours[tour_idx]
        
        new_tour = new_tours[tour_idx]
        
        best_tour_cost = problem.cal_tour_cost(new_tour)
        old_tour_cost = best_tour_cost

        for node_idx in xrange(len(new_tour)):
            
            old_node = new_tour[node_idx]
            
            if problem.obligatory_nodes.issuperset(set([old_node])):             
                continue
            
            best_tours = None
            
            for node in nodes_not_in_tours:
                new_tour[node_idx] = node
                        
                # check if this covering all customers
                if problem.isFeasibleTours(new_tours):
                    
                    #check cost improvement
                    new_tour_cost = problem.cal_tour_cost(new_tour)
                    
                    # if improvement, return success
                    if new_tour_cost < best_tour_cost:
                        best_tour_cost = new_tour_cost
                        best_tours = deepcopy(new_tours)
                        break
                        
                new_tour[node_idx] = old_node
                        
            # if have improvement
            if best_tours:
                
                giant_tour = problem.concat(best_tours)
                # try to remove node
                better_giant_tour = problem.remove_node(giant_tour)
                
                if len(better_giant_tour) < len(giant_tour):
                    cost, backtrack = problem.split(better_giant_tour)
                    
                    new_ind.giant_tour = better_giant_tour
                    new_ind.tours = problem.extract_tours(better_giant_tour, backtrack)
                    new_ind.fitness.values = cost,
                else:
                    new_ind.giant_tour = giant_tour
                    new_ind.tours = best_tours                                            
                    new_ind.fitness.values = old_fitness - old_tour_cost + best_tour_cost,
                    
                for i in xrange(len(new_ind)):
                    if new_ind[i] == old_node:
                        new_ind[i] = node
                    
                    elif new_ind[i] == node:
                        new_ind[i] = old_node
                
                return True, new_ind
            
                
    return False, None
        

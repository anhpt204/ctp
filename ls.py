'''
Created on Sep 8, 2015
@author: pta
'''

from ls_moves import *
from setting import MAX_TRAILS_LS

# local search
def ls_prins(problem, individual, gen):
    '''
    A Simple and Effective Evolutionary Algorithm for the Vehicle Routing Problem, Prins, 2001
    '''
#     move_operators = [move1, move2, move3, move4, move5, move6, move7, move8, move9]
    move_operators=[move1, move8, move9]
    
    tours_len = len(individual.tours)
    tours = individual.tours
    best_cost = individual.fitness.values[0]
    best_tours = individual.tours
    improvement = False
    
    for tour_i in xrange(tours_len):
        tour1_tmp = [0] + tours[tour_i] + [0]
        for i in xrange(len(tour1_tmp) -1):
            u, x = tour1_tmp[i], tour1_tmp[i+1]
            for tour_j in xrange(tours_len):
                tour2_tmp = [0] + tours[tour_j] +  [0]
                for j in xrange(len(tour2_tmp) - 1):
                    v, y = tour2_tmp[j], tour2_tmp[j+1]
                    # move operators
                    for move in move_operators:
                                                
                        move_success, temp_tours = move(individual, tour_i, tour_j, i, j, u, v, x, y)
                        
                        
                        if move_success and problem.isFeasibleSolution(temp_tours):
#                             print tour_i, tour_j, i, j, temp_tours
                            cost = problem.get_solution_cost(temp_tours)
                            # if improvement
                            if cost < best_cost:
                                best_cost = cost
                                best_tours = temp_tours[:]
                                improvement = True
                                
                                # update move frequency
                                
                                if problem.moves_freq.has_key(move.__name__):
                                    problem.moves_freq[move.__name__] += 1
                                else:
                                    problem.moves_freq[move.__name__] = 1
                                
                                break
#                 if improvement:
#                     break
#             if improvement:
#                 break
#         if improvement:
#             break
    # try LS4
    if not improvement:
        ls4_improvement, new_ind = move10(problem, individual)
        if ls4_improvement:
            if problem.moves_freq.has_key('move10'):
                problem.moves_freq['move10'] += 1
            else:
                problem.moves_freq['move10'] = 1
                 
#             print 'ls4: ', new_ind
            return new_ind
    
    if improvement:
        print 'best_tours: ', best_tours
        individual.tours = best_tours[:]
        old_giant_tour = individual.giant_tour
        new_giant_tour = problem.concat(best_tours)
        changes = {}
        for k, v in zip(old_giant_tour, new_giant_tour):
            changes[k] = v       
        
        # change individual response to new giant tour
        for i in xrange(len(individual)):
            k = individual[i]
            if changes.has_key(k):
                individual[i] = changes[k]
        
        print 'ind: ', individual
        individual.giant_tour = new_giant_tour
        individual.fitness.values = best_cost,
        
    return individual 


def ls_prins_vrp(problem, individual, gen):
    '''
    A Simple and Effective Evolutionary Algorithm for the Vehicle Routing Problem, Prins, 2001
    '''
#     move_operators = [move1, move2, move3, move4, move5, move6, move7, move8, move9]
    move_operators=[move1, move8, move9]
    
    tours_len = len(individual.tours)
    tours = individual.tours
    best_cost = individual.fitness.values[0]
    best_tours = individual.tours
    improvement = False
    
    for tour_i in xrange(tours_len):
        tour1_tmp = [0] + tours[tour_i] + [0]
        for i in xrange(len(tour1_tmp) -1):
            u, x = tour1_tmp[i], tour1_tmp[i+1]
            for tour_j in xrange(tours_len):
                tour2_tmp = [0] + tours[tour_j] +  [0]
                for j in xrange(len(tour2_tmp) - 1):
                    v, y = tour2_tmp[j], tour2_tmp[j+1]
                    # move operators
                    for move in move_operators:
#                         if(not set(individual).issuperset(problem.obligatory_nodes)):
#                             print move.__name__
#                         print individual.tours
                        move_success, temp_tours = move(individual, tour_i, tour_j, i, j, u, v, x, y)
#                         print temp_tours

#                         giant_tour = problem.concat(temp_tours)
                        
#                         if(not set(giant_tour).issuperset(problem.obligatory_nodes)):
#                             print move.__name__
                            
                        if move_success and problem.isFeasibleSolution(temp_tours):
#                             print tour_i, tour_j, i, j, temp_tours
                            cost = problem.get_solution_cost(temp_tours)
                            # if improvement
                            if cost < best_cost:
                                best_cost = cost
                                best_tours = temp_tours[:]
                                improvement = True
                                
                                # update move frequency
                                
                                if problem.moves_freq.has_key(move.__name__):
                                    problem.moves_freq[move.__name__] += 1
                                else:
                                    problem.moves_freq[move.__name__] = 1
                                
#                                 break
#                 if improvement:
#                     break
#             if improvement:
#                 break
#         if improvement:
#             break
    # try LS4
    if not improvement:
        ls4_improvement, new_ind = move10_vrp(problem, individual)
        if ls4_improvement:
            if problem.moves_freq.has_key('move10'):
                problem.moves_freq['move10'] += 1
            else:
                problem.moves_freq['move10'] = 1
                  
#             print 'ls4: ', new_ind
            return new_ind
    
    if improvement:
#         print 'best_tours: ', best_tours
        individual.tours = best_tours[:]
        old_giant_tour = individual.giant_tour
        new_giant_tour = problem.concat(best_tours)
        
        del individual[len(new_giant_tour):]
        for i in xrange(len(individual)):
            individual[i]=new_giant_tour[i]

#         if not set(individual).issuperset(problem.obligatory_nodes):
#             print new_giant_tour
        
        individual.giant_tour = new_giant_tour
        individual.fitness.values = best_cost,
        
    return individual 

def ls_move14(problem, individual, num_ls, gen):
    tours_len = len(individual.tours)
    tours = individual.tours
    best_cost = individual.fitness.values[0]
    best_tours = individual.tours
    
    operators = [move1, move4]
    
    improvement = False
    
    for _ in xrange(MAX_TRAILS_LS):
        tour_i = random.randint(0, tours_len-1)
        # select tour_j != tour_i randomly
        tour_j = tour_i
        if tours_len > 1:
            while tour_j == tour_i:
                tour_j = random.randint(0, tours_len-1)
        
        # select two node in these tours
        i = random.randint(0, len(tours[tour_i])-1)
        j = random.randint(0, len(tours[tour_j])-1)
        u = tours[tour_i][i]
        v = tours[tour_j][j]
        
        for o in operators:
            move_success, temp_tours = o(individual, tour_i, tour_j, i, j, u, v, x=None, y=None)

            if move_success and problem.isFeasibleSolution(temp_tours):
#               print tour_i, tour_j, i, j, temp_tours
                cost = problem.get_solution_cost(temp_tours)
                # if improvement
                if cost < best_cost:
                    best_cost = cost
                    best_tours = temp_tours[:]
                    improvement = True
                    break
                    
    # try LS4
    if not improvement:
        ls4_improvement, new_ind = move10(problem, individual)
        if ls4_improvement:
            return new_ind
        
    if improvement:
        individual.tours = best_tours[:]
        old_giant_tour = individual.giant_tour
        new_giant_tour = problem.concat(best_tours)
        changes = {}
        for k, v in zip(old_giant_tour, new_giant_tour):
            changes[k] = v       
        
        # change individual response to new giant tour
        for i in xrange(len(individual)):
            k = individual[i]
            if changes.has_key(k):
                individual[i] = changes[k]
        
        individual.giant_tour = new_giant_tour
        individual.fitness.values = best_cost,
    
    return individual 

def LS2(problem, giant_tour, tours, cost):
    '''
    relocate a node to another tour in solution
    '''
#    new_ind = deepcopy(individual)
    old_fitness = cost
    new_tours = deepcopy(tours)
    tour_len = len(tours)
    
    best_dest_tour_idx = None
    best_dest_node_idx = None
    best_src_tour_idx = None
    best_src_node_idx = None
    best_cost = old_fitness
    
    # for each tour as a destination tour
    for dest_tour_idx in xrange(tour_len):
        # if we can add a node into this tour
        if len(tours[dest_tour_idx]) < problem.max_nodes_per_route:
            # add depot into tour to make it easier for re-calculating solution cost
            dest_tour = [0] + tours[dest_tour_idx] + [0]
            # with each tour as a source tour
            for src_tour_idx in xrange(tour_len):
                # if source tour is difference destination tour 
                if dest_tour_idx != src_tour_idx:
                    src_tour = [0] + tours[src_tour_idx] + [0]
                    # try to insert a node from source tour to destination tour
                    for dest_node_idx in xrange(1,len(dest_tour)):
                        dest_node = dest_tour[dest_node_idx]
                        for src_node_idx in xrange(1,len(src_tour)-1):
                            src_node = src_tour[src_node_idx]

#                             print src_node, src_tour
#                             print dest_node, dest_tour
                            # re-calculate solution cost
                            new_cost = old_fitness - problem.nodes[dest_tour[dest_node_idx-1]].cost_dict[dest_node] \
                            + problem.nodes[dest_tour[dest_node_idx-1]].cost_dict[src_node] + problem.nodes[src_node].cost_dict[dest_node] \
                            # for source tour
                            - (problem.nodes[src_tour[src_node_idx-1]].cost_dict[src_node] + problem.nodes[src_node].cost_dict[src_tour[src_node_idx+1]])
                            # if route is empty
                            if len(src_tour) > 3:
                                new_cost += problem.nodes[src_tour[src_node_idx-1]].cost_dict[src_tour[src_node_idx+1]]
                            # if better
                            if new_cost<best_cost:
                                best_cost = new_cost
                                best_src_tour_idx = src_tour_idx
                                best_src_node_idx = src_node_idx-1
                                best_dest_tour_idx = dest_tour_idx
                                best_dest_node_idx = dest_node_idx-1
                                
    if best_dest_tour_idx:
        node_relocated = new_tours[best_src_tour_idx][best_src_node_idx]
        new_tours[best_src_tour_idx].remove(node_relocated)
        new_tours[best_dest_tour_idx].insert(best_dest_node_idx, node_relocated)
        
        
    return new_tours, best_cost

def LS3(problem, giant_tour, tours, cost):
    '''
    swap two nodes, 
    return best improvement
    '''
    old_fitness = cost
    new_tours = deepcopy(tours)
    tour_len = len(tours)
    
    best_dest_tour_idx = None
    best_dest_node_idx = None
    best_src_tour_idx = None
    best_src_node_idx = None
    best_cost = old_fitness

    # for each source and destionation tour
    for src_tour_idx in xrange(tour_len):
        for dest_tour_idx in xrange(tour_len):
            src_tour = [0] + new_tours[src_tour_idx] + [0]
            dest_tour = [0] + new_tours[dest_tour_idx] + [0]
            
            if src_tour_idx == dest_tour_idx:
                continue
            
            # try to swap two nodes, one from source tour, another from destination tour
            for src_node_idx in xrange(1, len(src_tour)-1):
                for dest_node_idx in xrange(1,len(dest_tour)-1):
                    src_node = src_tour[src_node_idx]
                    dest_node = dest_tour[dest_node_idx]

#                     print src_node, src_tour
#                     print dest_node, dest_tour
                    
                    # calculate cost if swap these two nodes
                    new_cost = old_fitness  - (problem.nodes[src_tour[src_node_idx-1]].cost_dict[src_node] 
                                              + problem.nodes[src_node].cost_dict[src_tour[src_node_idx+1]]) 
                    
                    new_cost += (problem.nodes[src_tour[src_node_idx-1]].cost_dict[dest_node]
                                              + problem.nodes[dest_node].cost_dict[src_tour[src_node_idx+1]])
                    
                    new_cost -= (problem.nodes[dest_tour[dest_node_idx-1]].cost_dict[dest_node]
                                               + problem.nodes[dest_node].cost_dict[dest_tour[dest_node_idx+1]])
                    
                    new_cost += (problem.nodes[dest_tour[dest_node_idx-1]].cost_dict[src_node]
                                               + problem.nodes[src_node].cost_dict[dest_tour[dest_node_idx+1]])
                                            
                                            
                    # if improvement
                    if new_cost < best_cost:
                        best_cost = new_cost
                        best_src_tour_idx = src_tour_idx
                        best_src_node_idx = src_node_idx-1
                        best_dest_tour_idx = dest_tour_idx
                        best_dest_node_idx = dest_node_idx-1
    # if find a better
    if best_dest_tour_idx:
        # swap
        tmp_node = new_tours[best_src_tour_idx][best_src_node_idx]
        new_tours[best_src_tour_idx][best_src_node_idx] = new_tours[best_dest_tour_idx][best_dest_node_idx]
        new_tours[best_dest_tour_idx][best_dest_node_idx] = tmp_node
        
        
    return new_tours, best_cost
                        
                    
def LS1(problem, giant_tour, tours, cost):
    '''
    remove short route by combining two short route subjec to maximum number
    nodes on a route constraint
    
    return the first improvement
    '''            
    old_fitness = cost
    new_tours = deepcopy(tours)
    tour_len = len(tours)
    
    best_cost = old_fitness

    for tour1_idx in xrange(tour_len):
        # check if len of tour1 is smaller than max_node_per_tour
        if len(new_tours[tour1_idx]) < problem.max_nodes_per_route:
            tour1 = new_tours[tour1_idx]
            for tour2_idx in xrange(tour_len):
                if tour1_idx != tour2_idx \
                    and len(new_tours[tour1_idx]) + len(new_tours[tour2_idx]) < problem.max_nodes_per_route:
                    # combine two tour
                    tour2 = new_tours[tour2_idx]
                    # try 4 cases
                    # first case 0-0
                    cost = old_fitness - (problem.nodes[tour1[0]].cost_dict[0]
                                          + problem.nodes[0].cost_dict[tour2[0]]) \
                                        + problem.nodes[tour1[0]].cost_dict[tour2[0]]
                    # make a new tour
                    new_tour = [v for v in tour1]
                    new_tour.reverse()
                    new_tour = new_tour + tour2
                    # second 0-(-1)
                    tmp_cost = old_fitness - (problem.nodes[tour1[0]].cost_dict[0]
                                          + problem.nodes[0].cost_dict[tour2[-1]]) \
                                        + problem.nodes[tour1[0]].cost_dict[tour2[-1]]
                    if tmp_cost < cost:
                        cost = tmp_cost
                        new_tour = tour2 + tour1
                        
                    # third -1 -0
                    tmp_cost = old_fitness - (problem.nodes[tour1[-1]].cost_dict[0]
                                          + problem.nodes[0].cost_dict[tour2[0]]) \
                                        + problem.nodes[tour1[-1]].cost_dict[tour2[0]]
                    if tmp_cost < cost:
                        cost = tmp_cost
                        new_tour = tour1 + tour2
                        
                    # third -1 -1
                    tmp_cost = old_fitness - (problem.nodes[tour1[-1]].cost_dict[0]
                                          + problem.nodes[0].cost_dict[tour2[-1]]) \
                                        + problem.nodes[tour1[-1]].cost_dict[tour2[-1]]
                    if tmp_cost < cost:
                        cost = tmp_cost
                        new_tour = deepcopy(tour2)
                        new_tour.reverse()
                        new_tour = tour1 + new_tour
                        
                    if cost < best_cost:
                        # edit tour 1
                        new_tours[tour1_idx] = new_tour
                        # and delete tour 2
                        del new_tours[tour2_idx]
                                                
                        best_cost = cost
                        
                        return new_tours, best_cost
                
    return new_tours, best_cost

def LS4(problem, giant_tour, tours, cost):
    '''
    replace a node in a tour with another node outside of giant tour
    '''
    
    old_fitness = cost
    
    # get all nodes that are not in tours
    nodes_in_tours = set(giant_tour)
    nodes = range(1, len(problem.nodes))
    
    nodes_not_in_tours = set(nodes).difference(nodes_in_tours)

    # make a new tours
    new_tours = deepcopy(tours)  
    new_giant_tour = deepcopy(giant_tour)
    best_cost = cost    
                
    for tour_idx in xrange(len(tours)):
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
                if problem.is_tours_satisfy_covering_constraint(new_tours):
                    
                    #check cost improvement
                    new_tour_cost = problem.cal_tour_cost(new_tour)
                    
                    # if improvement, return success
                    if new_tour_cost < best_tour_cost:
                        
                        # try replace two nodes around this node
#                         sucss, new_new_tour, new_new_tour_cost = ls_next_node(problem, new_tour, new_tour_cost, node_idx, nodes_not_in_tours)
#                         if sucss:
#                             new_tour = new_new_tour
#                             new_tour_cost = new_new_tour_cost
                            
                        best_tour_cost = new_tour_cost
                        best_tours = deepcopy(new_tours)
                        break
                    
                # back to old node for next try
                new_tour[node_idx] = old_node
                        
            # if have improvement
            if best_tours:
                
                giant_tour = problem.concat(best_tours)
                # try to remove node
                better_giant_tour = problem.remove_node(giant_tour)
                
                # if have redundance node, re-calculate cost
                if len(better_giant_tour) < len(giant_tour):
                    cost, backtrack = problem.split(better_giant_tour)
                    
                    new_giant_tour = better_giant_tour
                    new_tours = problem.extract_tours(better_giant_tour, backtrack)
                    best_cost = cost
                else:
                    new_giant_tour = giant_tour
                    new_tours = best_tours                                            
                    best_cost = old_fitness - old_tour_cost + best_tour_cost
                    
                
                return new_tours, best_cost
            
                
    return new_tours, best_cost
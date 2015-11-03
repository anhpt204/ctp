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
                                
                                break
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
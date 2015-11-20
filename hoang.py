'''
Created on Nov 19, 2015

@author: anhpt4

implement metaheuristic ELS from Hoang's paper
'''
from ls import LS1, LS3, LS2, LS4
from random import sample
from copy import deepcopy
from ls_moves import move10

def ELS(problem, giant_tour, tours, cost):
    N = len(giant_tour)
#     tmp_ind = deepcopy(giant_tour)
    best_tours, best_cost = LS1(problem, giant_tour, tours, cost)
    best_giant_tour = problem.concat(best_tours)
    new_tours = deepcopy(tours)
    new_giant_tour = deepcopy(best_giant_tour)
    while True:
        for i in xrange(N):
            f_min = 10**10
            giant_tour_min = None
            tours_min = None
            for j in xrange(N):
                new_giant_tour = problem.concat(new_tours)

                N = len(new_giant_tour)
#                 assert len(new_giant_tour) == N, 'giant tour after concat has diffence length with individual'
                    
                u, v = sample(xrange(N), 2)
                if u != v:
                    # swap node at u and v
                    k = new_giant_tour[u]
                    new_giant_tour[u] = new_giant_tour[v]
                    new_giant_tour[v]=k
                    
                    # split
                    new_cost, backtrack = problem.split(new_giant_tour)
                    new_tours = problem.extract_tours(new_giant_tour,backtrack)
                    
                    new_tours, new_cost = LS1(problem, new_giant_tour, new_tours, new_cost)
                    new_giant_tour = problem.concat(new_tours)

                    new_tours, new_cost = LS3(problem, new_giant_tour, new_tours, new_cost)
                    new_giant_tour = problem.concat(new_tours)

                    new_tours, new_cost = LS2(problem, new_giant_tour, new_tours, new_cost)
                    new_giant_tour = problem.concat(new_tours)
                    
                    if new_cost < f_min:
                        f_min = new_cost
                        giant_tour_min = deepcopy(new_giant_tour)
                        tours_min = deepcopy(new_tours)
                        
            if f_min < best_cost:
                best_giant_tour = deepcopy(giant_tour_min)
                best_tours = deepcopy(tours_min)
                best_cost = f_min
                
        new_tours, new_cost = LS4(problem, best_giant_tour, best_tours, best_cost)
        
        
        if new_cost >= best_cost:
            return best_giant_tour, best_tours, best_cost
#         else:
#             new_giant_tour = problem.concat(new_tours)
#             return new_giant_tour, new_tours, new_cost
#         return best_giant_tour

if __name__ == '__main__':
    pass
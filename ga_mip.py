'''
Created on Nov 2, 2015

@author: pta

run VRP using GA with initial solution from MIP (Hoang) 
'''
from ga_vrp import GA_VRP
from os.path import join, basename
import glob
from problem import CTPProblem
import random
from ls import ls_prins_vrp
from hoang import ELS

problems_data_dir = 'data_ctp'
initial_solution_dir = 'SubSet'

problems = glob.glob(join(initial_solution_dir, '*.ctp'))

problems = [basename(p) for p in problems]

problems = [
#             'A1-1-25-75-6.ctp',
            'A2-20-100-100-4.ctp'
            ]
def run():
    for problem_name in problems:
        
        print problem_name
        # load data 
        problem = CTPProblem(data_path=join(problems_data_dir, problem_name))
        
        #load initial solutions
        lines = open(join(initial_solution_dir, problem_name), 'r').readlines()
        
        best_cost = 10**10
        best_solution=None
        
#         lines = lines[:2]
        n = len(lines)
        lines = [lines[i] for i in xrange(1, n, 2)]
        print len(lines)
        lines = random.sample(lines, 20)
        for i in xrange(len(lines)):
#             print i, 
            init_sol = [int(v) for v in lines[i].split()]
            
            # GA
            vrp_solver = GA_VRP(problem=problem, nodes=init_sol)            
            cost, ind = vrp_solver.run(0)
            # Hoang
#             ind = ELS()
            
            print 'cost: ', cost
#             print 'local search on best ind'        
#             ind = ls_prins_vrp(problem=problem, individual=ind,gen=0)
#             cost = ind.fitness.values[0]
#             print 'cost after LS: ', cost         

            if cost < best_cost:
                best_cost = cost
                best_solution = ind
            
#             if i == 11:
#                 break
        
            print i, cost, ind
            
        
        print 'best so far: ', best_cost, best_solution            
            
        break
            

if __name__ == '__main__':
    
    run()
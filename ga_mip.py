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

problems_data_dir = 'data_ctp'
initial_solution_dir = 'SubSet'

problems = glob.glob(join(initial_solution_dir, '*.ctp'))

problems = [basename(p) for p in problems]

problems = [
#             'A1-1-25-75-6.ctp',
            'A2-20-100-100-5.ctp'
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
#         lines = random.sample(lines, 20)
        for i in xrange(len(lines)):
#             print i, 
            init_sol = [int(v) for v in lines[i].split()]
            
            vrp_solver = GA_VRP(problem=problem, nodes=init_sol)
            
            cost, tours = vrp_solver.run(0)
            
            if cost < best_cost:
                best_cost = cost
                best_solution = tours
            
#             if i == 11:
#                 break
        
            print i, cost, tours
            
        print 'best so far: ', best_cost, best_solution            
        break
            

if __name__ == '__main__':
    
    run()
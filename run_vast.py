'''
Created on Dec 22, 2015

@author: anhpt4
'''
import datetime
from problem import MCTPProblem, GMCTPProblem
from os.path import join
from setting import *
from mctp import GA_MCTP
from copy import deepcopy
import sys

def run_mctp(input_file, output_file):
    time1 = datetime.datetime.now()
    file = join('/home/anhpt4/git/ctp/gmctp_vast_input', input_file)
    problem = MCTPProblem(data_path=file, max_tour_length=250)
        
    problem.max_nodes_per_route = 1000
        
    print problem.max_tour_length

    best_solution = None
    best_cost = MAX_VALUE
        
    best_runs =[]
    lines = []
    for job in xrange(JOBS):
        ga = GA_MCTP(problem, job)
        cost, tours = ga.run()
           
        best_runs.append(cost)
            
        if cost < best_cost:
            best_cost = cost
            best_solution = deepcopy(tours)
                
        lines.append('%s %.2f %.2f %d [%s] %s\n' %(input_file, 
                                               problem.best_cost,
                                               best_cost, 
                                               len(best_solution),
#                                                  d.seconds, 
                                               ' '.join([str(v) for v in best_runs]),
                                               str(best_solution),
#                                                  str(best_solution.tours)
                                               ))

#         print best_cost, best_solution
    time2 = datetime.datetime.now()
    duration = time2-time1
    
    lines.append(str(duration))
    
    f = open(join('mctp_out', output_file), 'w')
    f.writelines(lines)


def run_gmctp(input_file, output_file):
    time1 = datetime.datetime.now()
    file = join('/home/anhpt4/git/ctp/gmctp_vast_input', input_file)
    problem = GMCTPProblem(data_path=file, max_tour_length=250)
        
#     problem.max_nodes_per_route = 1000
    problem.max_tour_length = MAX_VALUE
    
    print problem.max_tour_length

    best_solution = None
    best_cost = MAX_VALUE
        
    best_runs =[]
    lines = []
    for job in xrange(JOBS):
        ga = GA_MCTP(problem, job)
        cost, tours = ga.run()
           
        best_runs.append(cost)
            
        if cost < best_cost:
            best_cost = cost
            best_solution = deepcopy(tours)
                
        lines.append('%s %.2f %.2f %d [%s] %s\n' %(input_file, 
                                               problem.best_cost,
                                               best_cost, 
                                               len(best_solution),
#                                                  d.seconds, 
                                               ' '.join([str(v) for v in best_runs]),
                                               str(best_solution),
#                                                  str(best_solution.tours)
                                               ))

#         print best_cost, best_solution
    time2 = datetime.datetime.now()
    duration = time2-time1
    
    lines.append(str(duration))
    
    f = open(join('gmctp_out', output_file), 'w')
    f.writelines(lines)



if __name__ == '__main__':
    run_gmctp('input.108', 'output.108')

#     if sys.argv[1] == 'mctp':
#         run_mctp(sys.argv[2], sys.argv[3])
#     elif sys.argv[1] == 'gmctp':
#         run_gmctp(sys.argv[2], sys.argv[3])
        

'''
Created on Dec 22, 2015

@author: anhpt4
'''
import datetime
from problem import MCTPProblem
from os.path import join
from setting import *
from mctp import GA_MCTP
from copy import deepcopy
import sys

def run_mctp(input_file, output_file):
    time1 = datetime.datetime.now()
    file = join('/home/hanu.nxhoai/pta/ctp/mctp_vast_input', input_file)
    problem = MCTPProblem(data_path=file, max_tour_length=250)
        
#    problem.max_nodes_per_route = 1000
#    problem.max_tour_length=MAX_VALUE
        
#    print problem.max_tour_length

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


if __name__ == '__main__':
#     run_mctp('input.1', 'output.1')

    if sys.argv[1] == 'mctp':
        run_mctp(sys.argv[2], sys.argv[3])
        

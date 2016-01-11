'''
Created on Dec 22, 2015

@author: anhpt4
'''
import datetime
from problem import MCTPProblem, GMCTPProblem, CTPProblem
from os.path import join
from setting import *
from mctp import GA_MCTP
from copy import deepcopy
import sys
import glob

# data_dir = '/home/hanu.nxhoai/pta/ctp'
data_dir = '/home/pta/git/ctp'

# data_mctp = 'data_mctp_vast'
# data_mctp1 = 'data_mctp1_vast'
# data_mctp2 = 'data_mctp2_vast'

# data_gmctp = 'data_gmctp_vast'
# data_gmctp1 = 'data_gmctp1_vast'
# data_gmctp2 = 'data_gmctp2_vast'

data_mctp = 'data_mctp'
data_mctp1 = 'data_mctp1'
data_mctp2 = 'data_test'

data_gmctp = 'data_gmctp'
data_gmctp1 = 'data_gmctp1'
data_gmctp2 = 'data_gmctp2'

def run_mctp(input_file, output_file):
    time1 = datetime.datetime.now()
    file = join(data_dir, data_mctp, input_file)
    problem = MCTPProblem(data_path=file)
        
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
    
def run_mctp1(input_file, output_file):
    time1 = datetime.datetime.now()
    file = join(data_dir, data_mctp1, input_file)
    problem = MCTPProblem(data_path=file)
        
    problem.max_nodes_per_route = 1000
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
    
    f = open(join('mctp1_out', output_file), 'w')
    f.writelines(lines)

def run_mctp2(input_file, output_file):
    time1 = datetime.datetime.now()
    file = join(data_dir, data_mctp2, input_file)
    problem = CTPProblem(data_path=file)
    print problem.name        
#    problem.max_nodes_per_route = 1000
    problem.max_tour_length=MAX_VALUE
        
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
    
    f = open(join('mctp2_out', output_file), 'w')
    f.writelines(lines)


def run_gmctp(input_file, output_file):
    time1 = datetime.datetime.now()
    file = join(data_dir, data_gmctp, input_file)
    problem = GMCTPProblem(data_path=file)
        
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

def run_gmctp1(input_file, output_file):
    time1 = datetime.datetime.now()
    file = join(data_dir, data_gmctp1, input_file)
    problem = GMCTPProblem(data_path=file)
        
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
    
    f = open(join('gmctp1_out', output_file), 'w')
    f.writelines(lines)

def run_gmctp2(input_file, output_file):
    time1 = datetime.datetime.now()
    file = join(data_dir, data_gmctp2, input_file)
    problem = GMCTPProblem(data_path=file)
        
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
    
    f = open(join('gmctp2_out', output_file), 'w')
    f.writelines(lines)


if __name__ == '__main__':
#     run_gmctp('input.108', 'output.108')
    
    run_mctp2('B2-20-100-100-5.ctp', 'test.out')
    
#      files = glob.glob1(data_mctp2, '*.ctp')
#      for file in files:
#          run_mctp2(file, file + '.out')

#     if sys.argv[1] == 'mctp':
#         run_mctp(sys.argv[2], sys.argv[3])
#     elif sys.argv[1] == 'mctp1':
#         run_mctp1(sys.argv[2], sys.argv[3])
#     elif sys.argv[1] == 'mctp2':
#         run_mctp2(sys.argv[2], sys.argv[3])
#     elif sys.argv[1] == 'gmctp':
#         run_gmctp(sys.argv[2], sys.argv[3])
#     elif sys.argv[1] == 'gmctp1':
#         run_gmctp1(sys.argv[2], sys.argv[3])
#     elif sys.argv[1] == 'gmctp2':
#         run_gmctp2(sys.argv[2], sys.argv[3])
        

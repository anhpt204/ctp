# GA + Local Search

import array
import random
import json

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from problem import CTPProblem
from util import split, extract_tours, get_cost, concat, get_all_solutions,\
    get_giant_tour
from os.path import join

from setting import *
from math import fabs
from ls_moves import *
from deap.algorithms import varOr, eaSimple, varAnd
from ls import ls_prins
from genetic import eaPTA, evolve
from mutations import mutLS, mutLS4
from crossovers import PMX
from __init__ import *

# load problem
# data_path = '/home/pta/projects/ctp/data_ctp/kroA-13-12-75-4.ctp'
problem = CTPProblem()
# problem.load_data(data_path)
toolbox = base.Toolbox()
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin, giant_tour=list, tours=list)

def initialize():
    # ignore depot
    IND_SIZE = problem.num_of_nodes + len(problem.obligatory_nodes) -1



    # Attribute generator
    toolbox.register("indices", random.sample, range(1,IND_SIZE+1), IND_SIZE)
    
    # Structure initializers
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
                                                    

# evaluate solution
def eval(individual):
    
    best_cost = 10**10
    best_tour = None
    best_backtrack = None
    # get giant tours of an individual
#     giant_tours = get_all_solutions(problem, individual)
    giant_tours = [get_giant_tour(problem, individual)]
    # get the best giant tour
    for giant_tour in giant_tours:    
        key = tuple(giant_tour)
        
        cost = None
        if giant_tour_cost.has_key(key):
            cost, backtrack = giant_tour_cost[key]
        else:  
            cost, backtrack = split(problem, giant_tour)
            giant_tour_cost[key] = (cost, backtrack)        
        
        if cost < best_cost:
            best_cost = cost
            best_tour = giant_tour[:]
            best_backtrack = backtrack[:]
                    
    # split tour and return total cost
    tours = extract_tours(best_tour, best_backtrack)
    
    individual.tours = tours

    individual.giant_tour = best_tour
        
    return best_cost,


toolbox.register("mate", PMX)
toolbox.register("ls", mutLS,problem=problem)
toolbox.register("ls4", mutLS4, problem=problem)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=INDPB)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", eval)


def run(job=0):
    random.seed(1000+job)

    pop = toolbox.population(n=POPSIZE)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    eaPTA(pop, toolbox, PCROSS, PMUTATION, PLOCALSEARCH, PLS4, NUM_GEN, stats=stats, 
                        halloffame=hof, verbose=VERBOSE)
    
    print 'run ', job, ': ', hof[0].fitness.values[0], ': ', problem.best_cost, 'size=',len(hof[0].giant_tour)
    
    print hof[0].giant_tour
    print hof[0].tours
    
    return hof[0].fitness.values[0], len(hof[0].giant_tour)

def ec_ls_run(job=0):
    random.seed(1000+job)

    pop = toolbox.population(n=POPSIZE)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    evolve(pop, toolbox, PCROSS, PMUTATION, ngen=NUM_GEN, stats=stats, halloffame=hof, verbose=VERBOSE)
    
    print 'run ', job, ': ', hof[0].fitness.values[0], ': ', problem.best_cost, 'size=',len(hof[0].giant_tour)
        
    print hof[0].giant_tour
    print hof[0].tours
    
    print 'local search...'
    new_ind = ls_prins(problem, hof[0])
    print new_ind.fitness.values[0]
    print new_ind.giant_tour
    print new_ind.tours

    return new_ind.fitness.values[0], len(new_ind.giant_tour)
    

import glob, os, datetime
if __name__ == "__main__":
    # load problem
    data_dir = '/home/pta/projects/ctp/data_ctp/A/'
    
    files = glob.glob(data_dir + '*.ctp')
    lines = []
    
    files = [os.path.join(data_dir, 'A2-10-50-150-6.ctp')]
    
    for file in files:
        time1 = datetime.datetime.now()
        file_name = os.path.basename(file)
        
        problem.load_data(file)
        initialize()
        print file_name, ': ', problem.best_cost
        best_x =[]
        best_size = 0
        best_cost = 10**10
        for job in xrange(JOBS):
            
            cost, size = run(job)
#             cost, size = ec_ls_run(job)
            
            if cost < best_cost:
                best_cost = cost
                best_size = size
#             best_x.append(best_cost)
            
        time2 = datetime.datetime.now()
        
        lines.append( file_name + " " + str(best_cost) + " " + str(problem.best_cost) + " "  + str(best_size)+ " "+ str(time2-time1) + '\n')

    setting = open('setting.py','r').read()
    
    f = open('test.txt', 'w')
    f.write(setting + '\n')
    f.writelines(lines)

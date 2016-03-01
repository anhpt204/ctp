'''
Created on Sep 8, 2015
@author: pta
'''
import random
from deap import tools, algorithms
from deap.algorithms import varAnd
from __init__ import *
from util import *
from setting import NUM_GEN


def computeFitness(problem, individual):
    best_cost = 10**10
    best_tour = None
    best_backtrack = None
    # get giant tours of an individual
#     giant_tours = get_all_solutions(problem, individual)
    giant_tours = [problem.get_giant_tour(individual)]
    # get the best giant tour
    for giant_tour in giant_tours:  
        key = tuple(giant_tour)
        
        cost = None
        if problem.giant_tour_cost.has_key(key):
            cost, backtrack = problem.giant_tour_cost[key]
        else:  
            cost, backtrack = problem.split(giant_tour)
            problem.giant_tour_cost[key] = (cost, backtrack)
            
        if cost < best_cost:
            best_cost = cost
            best_tour = giant_tour[:]
            best_backtrack = backtrack[:]
                    
    # split tour and return total cost
    tours = problem.extract_tours(best_tour, best_backtrack)
    
    individual.tours = tours

    individual.giant_tour = best_tour
    # assign to individual
    individual.fitness.values = best_cost,
#     individual.tours = tours

def varAndLS(population, toolbox, cxpb, mutpb, num_ls, gen):
    
    offspring = [toolbox.clone(ind) for ind in population]
    
    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i-1], offspring[i] = toolbox.mate(offspring[i-1], offspring[i])
            del offspring[i-1].fitness.values, offspring[i].fitness.values
    
    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values
    
#     lspb = float(gen)/(NUM_GEN * 20)
# # #     lspb = 0
#     for i in range(len(offspring)):
#         if random.random() < lspb:
#             offspring[i], = toolbox.ls(individual=offspring[i], gen=gen)
            
#     for i in range(len(offspring)):
#         if random.random() < lspb:
#             offspring[i], = toolbox.ls4(individual=offspring[i], num_ls=num_ls, gen=gen)
    
    return offspring

def varAndSCP(population, toolbox, cxpb, mutpb, gen):
    
    offspring = [toolbox.clone(ind) for ind in population]
    
    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i-1], offspring[i] = toolbox.mate(offspring[i-1], offspring[i])
            del offspring[i-1].fitness.values, offspring[i].fitness.values
    
    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values
    
#     lspb = float(gen)/(NUM_GEN * 20)
# #     lspb = 0s
#     for i in range(len(offspring)):
#         if random.random() < lspb:
#             offspring[i], = toolbox.ls(individual=offspring[i], num_ls=num_ls, gen=gen)
            
#     for i in range(len(offspring)):
#         if random.random() < lspb:
#             offspring[i], = toolbox.ls4(individual=offspring[i], num_ls=num_ls, gen=gen)
    for i in range(len(offspring)):
        nodes = [j+1 for j in xrange(len(offspring[i])) if offspring[i][j]==1]
        offspring[i].giant_tour = nodes
        
    return offspring

def varAndVRP(population, toolbox, cxpb, mutpb, gen):
    
    offspring = [toolbox.clone(ind) for ind in population]
    # Apply crossover and mutation on the offspring
#     print 'crossover...'
    for i in range(0, len(offspring)):
        if random.random() < cxpb:
            p1,p2 = random.sample(offspring, 2)

            offspring[i] = toolbox.mate(p1, p2)
            del offspring[i].fitness.values
    
#     for i in range(0, len(offspring)): 
#         if len(offspring[i]) != len(set(offspring[i])):
#             print offspring[i]
            
            
#     for i in range(len(offspring)):
#         if random.random() < mutpb:
#             offspring[i], = toolbox.mutate(offspring[i])
#             del offspring[i].fitness.values
    
#     lspb = float(gen)/100
#     print 'mutation...'
    lspb = 1.0
    for i in range(len(offspring)):
        if random.random() < lspb:
            ind = deepcopy(offspring[i])
#             print offspring[i]
            offspring[i], = toolbox.ls(individual=offspring[i], gen=gen)
#             
#             if offspring[i] == None:
#                 print ind
            
#     for i in range(len(offspring)):
#         if random.random() < lspb:
#             offspring[i], = toolbox.ls4(individual=offspring[i], num_ls=num_ls, gen=gen)
    
    return offspring

def varAndPTA(population, toolbox, cxpb, mutpb, lspb, lspb4, num_ls, gen):
    """
    """
    offspring = [toolbox.clone(ind) for ind in population]
    
    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i-1], offspring[i] = toolbox.mate(offspring[i-1], offspring[i])
            del offspring[i-1].fitness.values, offspring[i].fitness.values
            
        if random.random() < mutpb:
            offspring[i-1], = toolbox.mutate(offspring[i-1])
            del offspring[i-1].fitness.values
        
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values
            
        ls_pb = 0 #float(gen)/(NUM_GEN*100)
#         print i
        if random.random() < ls_pb:
            offspring[i-1], = toolbox.ls(individual=offspring[i-1], num_ls=num_ls, gen=gen)
            
        if random.random() < ls_pb:
            offspring[i], = toolbox.ls(individual=offspring[i], num_ls=num_ls, gen=gen)
            
        if random.random() < ls_pb:
            offspring[i-1], = toolbox.ls4(individual=offspring[i-1], num_ls=num_ls, gen=gen)
        if random.random() < ls_pb:
            offspring[i], = toolbox.ls4(individual=offspring[i], num_ls=num_ls, gen=gen)
    
    return offspring


def eaPTA(population, toolbox, cxpb, mutpb, lspb, lsbp4, ngen, stats=None, halloffame=None, verbose=__debug__):
    
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals', 'num_ls4', 'num_ls4_imp'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    num_ls = [[0,0]]

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), num_ls4=num_ls[0][0], num_ls4_imp=num_ls[0][1],**record)
    if verbose:
        print logbook.stream
    
    # Begin the generational process
    for gen in range(1, ngen+1):
        num_ls.append([0,0])
        # Select the next generation individuals
#         offspring = toolbox.select(population, len(population))
        
        # Vary the pool of individuals
#         offspring = varAndPTA(population, toolbox, cxpb, mutpb, lspb, lsbp4, num_ls, gen)
#         offspring = varAndLS(population, toolbox, cxpb, mutpb, num_ls, gen)
        offspring = algorithms.varAnd(population, toolbox, cxpb, mutpb)
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)
            
        # Replace the current population by the offspring
        population[:] = offspring
        
        # elitism
        t = random.randint(0, len(population)-1)
#         t = 0
        population[t] = halloffame[0]
#         print halloffame[0].fitness.values[0]
        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind),num_ls4=num_ls[gen][0], num_ls4_imp=num_ls[gen][1],  **record)
        if verbose:
            print logbook.stream        

    return population, logbook

def evolve(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):
   
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print logbook.stream

    # Begin the generational process
    for gen in range(1, ngen+1):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))
        
        # Vary the pool of individuals
        offspring = varAnd(offspring, toolbox, cxpb, mutpb)
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)
            
        # Replace the current population by the offspring
        population[:] = offspring
        
         # elitism
        t = random.randint(0, len(population)-1)
#         t = 0
        population[t] = halloffame[0]
        
        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print logbook.stream        

    return population, logbook
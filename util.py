'''
Created on Aug 18, 2015

@author: pta
'''
from os.path import join, basename
import glob
from setting import MAX_TRAILS
from copy import deepcopy




    
def format_data():
    data_dir = '/home/pta/projects/ctp/data_ctp'
    ctp_files = glob.glob(join(data_dir, '*.ctp'))
    for file in ctp_files:
        
        file_name = basename(file)
        
        lines = open(file, 'r').readlines()
        vs = [int(x) for x in lines[0].split()]
        
        tmp = file_name[:4].lower()
        
        new_file_name = ''
        if tmp == 'kroa':
            new_file_name = 'A'
        elif tmp == 'krob':
            new_file_name = 'B'
        elif tmp == 'kroc':
            new_file_name = 'C'
        else:
            new_file_name = 'D'
            
        size = sum(vs[:3])
        if size==200:
            new_file_name += '2'
        else:
            new_file_name += '1'
            
        # |T|
        new_file_name += '-'+str(vs[2])
        # |V|
        new_file_name += '-' + str(vs[0] + vs[2])
        new_file_name += '-' + str(vs[1])
        new_file_name += '-' + str(vs[3]) + '.ctp'
        
        open(join(data_dir, new_file_name), 'w').writelines(lines)
        
def cover_all_customers(problem, tours):
    '''
    return True  if tours cover all customers, else return False
    '''
    covering_set = set()
    
    for tour in tours:
        for node in tour:
            
            covered_customers = problem.get_set_of_customers_covered_by(node)
            
            covering_set = covering_set.union(covered_customers)
            
    if len(covering_set) == problem.num_of_customers:
        return True
    else:
        return False
    
def get_all_solutions(problem, individual, gen):
    '''
    get all solution of an individual
    '''
    covering = []
    solutions = []
    n = len(individual)
    
    for _ in xrange(n):
        covering.append(set())
        solutions.append([])
        
    for i in xrange(n):
        node = individual[i]
        # if node is in obligatory nodes then insert it into solutions
        if problem.obligatory_nodes.issuperset(set([node])):
            for solution in solutions:
                solution.append(node)
            continue
                
        # get all customers that are covered by this node
        covered_customers = problem.get_set_of_customers_covered_by(node)
        for j in xrange(i+1):
            if not covered_customers.issubset(covering[j]):
                solutions[j].append(node)
                covering[j].update(covered_customers)
            
    giant_tours = []
    giant_tours_set = []
    
    n = len(solutions)
    for i, solution, covered in zip(xrange(n),solutions, covering):
        if len(covered) == problem.num_of_customers:
            
            solution_set = set(solution)
            
            if len(giant_tours_set) > 0 and giant_tours_set[-1].issuperset(solution_set):            
                giant_tours_set[-1] = solution_set
                giant_tours[-1] = solution
            else:
                giant_tours.append(solution)
                giant_tours_set.append(set(solution))
                
    new_giant_tours = []

    for giant_tour in giant_tours:
        new_giant_tours.append(remove_node(problem, giant_tour))
    
    return new_giant_tours
        
def minimize_giant_tour(problem, tour):
    '''
    remove nodes that are redundent
    '''        
    giant_tours = [tour]
    optimal_giant_tours =[False]
    i = 0
    while True:
        giant_tour = giant_tours[i]
        optimal_giant_tours[i] = False
        is_optimal = True
        # for each node in giant-tour
        for node in giant_tour:
            if problem.obligatory_nodes.issuperset(set([node])):
                continue
            # calculate covering set if node is not in giant_tour
            covering_set = set()
            for anode in giant_tour:
                if anode != node:
                    covering_set.update(problem.get_set_of_customers_covered_by(anode))
            
            # if node is redundent, make a new giant_tour by removing this node
            if len(covering_set) == problem.num_of_customers:
                is_optimal = False
                new_giant_tour = deepcopy(giant_tour)
                new_giant_tour.remove(node)
                
                # append new giant tour, so that it will be minimized for the next some steps
                giant_tours.append(new_giant_tour)
                optimal_giant_tours.append(True)
        
        # if this giant_tour is optimal
        if is_optimal:
            optimal_giant_tours[i] = True
            
        i += 1
        
        if i == len(giant_tours) or i == 100:
            break
        
    # get minimal giant tours
    m_giant_tours = []
    for giant_tour, is_optimal in zip(giant_tours, optimal_giant_tours):
        if is_optimal:
            m_giant_tours.append(giant_tour)
    
    return m_giant_tours
         
    
def get_giant_tours(problem, individual):
    '''
    get giant tours of an individual
    try MAX_TRAILS times
    '''
    giant_tours =[]
#     MAX_TRAILS = 20
    for start_i in xrange(MAX_TRAILS):
        # get tour
        covering_set = set()
        tour = []
        
        # append nodes before start_i that in T into tour
        for node_id in individual[:start_i]:
            if problem.obligatory_nodes.issuperset(set([node_id])):
                tour.append(node_id)

        i = start_i
        while True:
            # infeasible
            if i >= len(individual):
                return giant_tours
            
            node_id = individual[i]
            i+=1
            # check if node belong to obligatory nodes
            if problem.obligatory_nodes.issuperset(set([node_id])):
                tour.append(node_id)
                continue
            
            covered_customers = problem.get_set_of_customers_covered_by(node_id)
            
            if covered_customers.issubset(covering_set):
                continue
            
            # update tour
            tour.append(node_id)
            
            # update covering set
            covering_set = covering_set.union(covered_customers)
            
            if len(covering_set) == problem.num_of_customers:
                break
            
            
            
        # append all remaining nodes in individual that also in obligatory nodes into tour
        for node_id in individual[i:]:
            if problem.obligatory_nodes.issuperset(set([node_id])):
                tour.append(node_id)

        giant_tours.append(tour)
        
    return giant_tours



    
if __name__ == '__main__':
    format_data()
                
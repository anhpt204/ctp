'''
Created on Aug 18, 2015

@author: pta
'''
from os.path import join, basename
import glob
from setting import MAX_TRAILS
from copy import deepcopy

def is_valid_solution(problem, tours):
    '''
    check constraints of a solution
    '''
    # check tour length
    for tour in tours:
        if len(tour) > problem.max_nodes_per_route:
            return False
    return True

def split(problem, tour):
    '''
    basic splitting algorithm 'tour splitting algorithms for vehicle routing problem' - Prins
    '''
    t = len(tour)
    # V[j] = cost of shortest path from node 0 to node j
    V = []
    # predec[j] predecessor of tour[j] 
    predec = [-1]*(t+1)
    # initialize
    V.append(None)
    for _ in xrange(t):
        V.append(10**10)
    
    V[0] = 0
    predec[0] = 0
    
    for i in xrange(1, t + 1):
        j = i
        load = 0
        node_i = tour[i-1]
        cost = 0
            
        while True:
            node_j = tour[j-1]
            load += problem.nodes[node_i].load
#             if node_j == 0:
#             print node_i, node_j, tour
                
            if i == j:
                cost = problem.nodes[0].cost_dict[node_i] \
                + problem.nodes[node_i].visited_cost \
                + problem.nodes[node_i].cost_dict[0]
            
            else:
                cost = cost - problem.nodes[tour[j-2]].cost_dict[0] \
                + problem.nodes[tour[j-2]].cost_dict[node_j] \
                + problem.nodes[node_j].visited_cost \
                + problem.nodes[node_j].cost_dict[0]
                
            if cost <= problem.vehicle_capacity \
            and load <= problem.max_nodes_per_route \
            and V[i-1] + cost < V[j]:
            
                V[j] = V[i-1] + cost
                predec[j] = i-1
                
            j += 1
            
            if j > t or load > problem.max_nodes_per_route or cost > problem.vehicle_capacity:
                break
              
    return V[t], predec

def extract_tours(giant_tour, predec):
    temp_tour = [0] + giant_tour
    tours = []
    t = len(temp_tour)-1
    j = t
    while True:
        T = []
        tours.append(T)
        i = predec[j]
        for k in xrange(i+1, j+1):
            T.append(temp_tour[k])
        j = i
        
        if i == 0:
            break
    tours.reverse()
    return tours
    
def concat(tours):
    '''
    concatenate tours into a giant tour
    '''
    giant_tour = tours[0]
    for tour in tours[1:]:
        giant_tour = giant_tour + tour
    return giant_tour
    
def get_cost(problem, tours):
    '''
    calculate cost of tours
    '''
    total_cost = 0
    for tour in tours:
        
        total_cost += get_tour_cost(problem, tour)
        
    return total_cost

def get_tour_cost(problem, tour):
    '''
    calculate cost of a tour
    '''
    temp_tour = [0] + tour + [0]
    tour_cost = 0
    # cost from node i to node j in the tour
    for i,j in zip(temp_tour[:-1], temp_tour[1:]):
#             print i, j
        tour_cost += problem.nodes[i].cost_dict[j]
    return tour_cost
    
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


def remove_node(problem, giant_tour):
    '''
    remove a redundant node from a giant tour
    '''
    have_redundant_node = False
    for node in giant_tour:
        # if it is a node in obligatory nodes, then jump to a next node
        if problem.obligatory_nodes.issuperset(set([node])):
            continue
        # get covering set of all remaining nodes:
        covering_set=set()
        for other_node in giant_tour:
            if other_node != node and not problem.obligatory_nodes.issuperset(set([other_node])):
                covering_set.update(problem.get_set_of_customers_covered_by(other_node))
                
        if len(covering_set) == problem.num_of_customers:
            have_redundant_node = True
            new_giant_tour = deepcopy(giant_tour)
            new_giant_tour.remove(node)
            return remove_node(problem, new_giant_tour)
        
    if not have_redundant_node:
        return giant_tour
            
        
    
def get_giant_tour(problem, individual):
    '''
    scan from left to right to extract a giant tour
    '''
    giant_tour = []
    i = 0
    covering_set = set()
    
    while True:
        node_id = individual[i]
        i += 1
        # check if node belong to obligatory nodes
        if problem.obligatory_nodes.issuperset(set([node_id])):
            giant_tour.append(node_id)
            continue
        
        covered_customers = problem.get_set_of_customers_covered_by(node_id)
        
        if covered_customers.issubset(covering_set):
            continue
        
        # update tour
        giant_tour.append(node_id)
        
        # update covering set
        covering_set = covering_set.union(covered_customers)
        
        if len(covering_set) == problem.num_of_customers:
            break
    
    # append all remaining nodes in individual that also in obligatory nodes into tour
    for node_id in individual[i:]:
        if problem.obligatory_nodes.issuperset(set([node_id])):
            giant_tour.append(node_id)
            
    giant_tour = remove_node(problem, giant_tour)
            
    individual.giant_tour = giant_tour
    
    return giant_tour

def calculate_tours_cost(problem, tours, job):
    '''
    calculate cost of a solution with explain detail
    '''
    f = open('cal_tours_cost.' + str(job), 'w')
    f.write(str(tours) +'\n')
    
    cost = 0
    for tour in tours:
        full_tour = [0] + tour + [0]
        for node1, node2 in zip(full_tour[:-1], full_tour[1:]):
            distance = problem.nodes[node1].cost_dict[node2]
            
            line = '%s %s %s\n' %(node1, node2, distance)
            f.write(line)
            
            cost += distance
            
    f.write(str(cost))
    f.close()
    
if __name__ == '__main__':
    format_data()
                
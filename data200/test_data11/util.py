'''
Created on Aug 18, 2015

@author: pta
'''
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
                
'''
Created on Aug 17, 2015
@author: pta
'''
from os.path import basename, join
from copy import deepcopy
from setting import MAX_VALUE
import random

class CTPNode():
    '''
    problem definition is by paper "The generalized Covering Salesman Problem" - Bruce Golden
    '''
    def __init__(self, id, x=0, y=0,visited_cost=0, coverage_demand=1, load=1):
        # id of node
        self.id = id
        
        self.x=x
        self.y=y
        # list of nodes that covered by this node
        self.cover_list = []
        
        # cost to go from this node to other node. It is a dict in form of {node_id:cost}
        self.cost_dict = {}
        
        # fixed cost associated with visiting this node
        self.visited_cost = visited_cost
        
        # a solution is feasible if this node is covered at least coverage_demand times
        self.coverage_demand = coverage_demand
        
        self.load = load
        
    def clone(self):
        node = CTPNode(self.id, self.x, self.y, self.visited_cost, self.coverage_demand, self.load)
        node.cover_list = deepcopy(self.cover_list)
        node.cost_dict = deepcopy(self.cost_dict)
        return node 
        
class CTPProblem():
    def __init__(self, data_path, max_tour_length=100000, load_data_from_file=True):
        self.nodes = []
        self.num_of_vehicles = 1
        self.max_nodes_per_route=0
        self.obligatory_nodes = set([])
        self.num_of_nodes = None 
        self.num_of_customers = None
        self.max_tour_length = max_tour_length
        self.best_cost = 0
        self.giant_tour_cost={}
        self.n_same_giant_tour = 0
        
        self.moves_freq = {}
        
        self.nodes_covering_customer={}
        if load_data_from_file:
            self.load_data(data_path)
        
    def load_data(self, data_path):
        self.data_path = data_path
        self.name = basename(data_path)
        
        lines = open(data_path, 'r').readlines()
        
        xs = [int(x) for x in lines[0].split()]
        self.num_of_nodes = xs[0]
        self.num_of_customers = xs[1]
        obligatory_node = xs[2]
        
        self.max_nodes_per_route=xs[3]
        
        
        if len(xs)>4:
            self.best_cost = xs[4]
        else:
            self.best_cost = 0
        
        self.obligatory_nodes = set(range(1,obligatory_node))
        
        # init    
        for l in xrange(self.num_of_customers):
            self.nodes_covering_customer[l]=set()

        # initialize nodes
        self.nodes = []
        for i in xrange(self.num_of_nodes + obligatory_node):
            node = CTPNode(id=i, visited_cost=0, coverage_demand=0)
            self.nodes.append(node)
            
        # load cost matrix
        i = 1
        line = lines[i]
        while not line.isspace():
            xs = line.split()
            id1, id2 = [int(x) for x in xs[:2]]
            distance = float(xs[-1])
            self.nodes[id1].cost_dict[id2] = distance
            self.nodes[id2].cost_dict[id1] = distance
            
            i += 1
            line = lines[i]
        
        # load covering matrix
        i += 1
        for line in lines[i:]:
            xs = [int(x) for x in line.split()]
            for i in xrange(self.num_of_customers):
                if xs[i+1] == 1:
                    self.nodes[xs[0]].cover_list.append(i)
                    self.nodes_covering_customer[i].update([xs[0]])
                    
    def get_set_of_customers_covered_by(self, node_id):
        '''
        get a set of customers that covered by a node (node_id)
        '''
        return set(self.nodes[node_id].cover_list)
    
    def get_set_of_customers_covered_by_giant_tour(self, giant_tour):
        '''
        get a set of customers that covered by a node (node_id)
        '''
        covering_set = set()
        for node in giant_tour:
            covering_set.update(set(self.nodes[node].cover_list))
            
        return covering_set

    def is_giant_tour_satisfy_covering_constraint(self, giant_tour):
        
        # get covering set of all remaining nodes:
        covering_set=set()
        
        for node in giant_tour:
            # if it is a node in obligatory nodes, then jump to a next node
            if self.obligatory_nodes.issuperset(set([node])):
                continue
        
            covering_set.update(self.get_set_of_customers_covered_by(node))
                
        if len(covering_set) == self.num_of_customers:
            return True
        
        return False

    def is_tours_satisfy_covering_constraint(self, tours):
        
        # get covering set of all remaining nodes:
        covering_set=set()
        for tour in tours:
            for node in tour:
                # if it is a node in obligatory nodes, then jump to a next node
                if self.obligatory_nodes.issuperset(set([node])):
                    continue
            
                covering_set.update(self.get_set_of_customers_covered_by(node))
                
        if len(covering_set) == self.num_of_customers:
            return True
        
        return False
    
    def isFeasibleSolution(self, tours):
        '''
        check constraints of a solution (tours)
        '''
        solution_len = 0
        set_nodes = set()
        # check tour length
        for tour in tours:
            solution_len += len(tour)
            set_nodes.update(set(tour))
            if len(tour) > self.max_nodes_per_route:
                return False
            
        # check dupblicate nodes
        if len(set_nodes) != solution_len:
            return False
        # check tour length
        return True
    
    def isSatisfyTourLength(self, tours):
        '''
        check tour length constraint
        '''
        for tour in tours:
            cost = self.cal_tour_cost(tour)
            if cost > self.max_tour_length:
                return False
        return True
    
    
    
    def old_split(self, tour):
        '''
        basic splitting algorithm 'tour splitting algorithms for vehicle routing problem' - Prins
        '''
    #     print tour
        
        t = len(tour)
        # V[j] = cost of shortest path from node 0 to node j
        V = []
        # predec[j] predecessor of tour[j] 
        predec = [-1]*(t+1)
        # initialize
        V.append(None)
        for _ in xrange(t):
            V.append(MAX_VALUE)
        
        V[0] = 0
        predec[0] = 0
        
        for i in xrange(1, t + 1):
            j = i
            load = 0
            node_i = tour[i-1]
            cost = 0
                
            while True:
                node_j = tour[j-1]
                load += self.nodes[node_i].load
    #             if node_j == 0:
    #             print node_i, node_j, tour
                    
                if i == j:
                    cost = self.nodes[0].cost_dict[node_i] \
                    + self.nodes[node_i].visited_cost \
                    + self.nodes[node_i].cost_dict[0]
                    
#                     if cost > self.max_tour_length:
#                         return MAX_VALUE, predec
                
                else:
                    cost = cost - self.nodes[tour[j-2]].cost_dict[0] \
                    + self.nodes[tour[j-2]].cost_dict[node_j] \
                    + self.nodes[node_j].visited_cost \
                    + self.nodes[node_j].cost_dict[0]
                    
                if cost <= self.max_tour_length \
                    and load <= self.max_nodes_per_route \
                    and V[i-1] + cost < V[j]:
                
                    V[j] = V[i-1] + cost
                    predec[j] = i-1
                    
                j += 1
                
                if j > t or load > self.max_nodes_per_route or cost > self.max_tour_length:
                    break
                  
        return V[t], predec
    
    def extract_tours(self, giant_tour, predec):
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
    
    def split(self, tour):
        giant_tour = [0] + tour
        
        t = len(giant_tour)
        V=[10**10]*t
        P = [-1]*t
        V[0] = 0
        P[0] = 0
        
        for i in xrange(1, t):
            j = i 
#             load = 0
            num_node_per_tour = 0
            node_i = giant_tour[i] 
            while True:
                node_j = giant_tour[j]
#                 load += self.nodes[j].load
                num_node_per_tour += 1
                
                if i == j:
                    cost = self.nodes[0].cost_dict[node_i] + self.nodes[node_i].visited_cost + self.nodes[node_i].cost_dict[0]
                else:
                    node_pre_j = giant_tour[j-1] 
                    cost = cost - self.nodes[node_pre_j].cost_dict[0] \
                        + self.nodes[node_pre_j].cost_dict[node_j] + self.nodes[node_j].visited_cost \
                        + self.nodes[node_j].cost_dict[0]
                        
                if cost <= self.max_tour_length \
                    and V[i-1] + cost < V[j] \
                    and num_node_per_tour <= self.max_nodes_per_route :
                    
                    V[j] = V[i-1]+cost
                    P[j] = i-1
                
                j += 1
                
                if j == t or cost > self.max_tour_length \
                    or num_node_per_tour > self.max_nodes_per_route:
                    break
                
        return V[t-1],P
                
        
    def concat(self, tours):
        '''
        concatenate tours into a giant tour
        '''
        giant_tour = tours[0]
        for tour in tours[1:]:
            giant_tour = giant_tour + tour
            
        return giant_tour
        
    def get_solution_cost(self, tours):
        '''
        calculate cost of tours
        '''
        total_cost = 0
        for tour in tours:
            
            total_cost += self.cal_tour_cost( tour)
            
        return total_cost
    
    def cal_tour_cost(self, tour):
        '''
        calculate cost of a tour
        '''
        temp_tour = [0] + tour + [0]
        tour_cost = 0
        # cost from node i to node j in the tour
        for i,j in zip(temp_tour[:-1], temp_tour[1:]):
    #             print i, j
            tour_cost += self.nodes[i].cost_dict[j]
        return tour_cost
    
    def remove_node(self, giant_tour):
        '''
        remove a redundant node from a giant tour
        '''
        best_cost = 10**10
        best_node=None
        
        for node in giant_tour:
            # if it is a node in obligatory nodes, then jump to a next node
            if self.obligatory_nodes.issuperset(set([node])):
                continue
            new_giant_tour = deepcopy(giant_tour)
            new_giant_tour.remove(node)
                    
            if self.is_giant_tour_satisfy_covering_constraint(new_giant_tour):
                cost, backtrack = self.split(new_giant_tour)
                
                if cost < best_cost:
                    best_cost=cost
                    best_node=node

        if best_node:
            new_giant_tour=deepcopy(giant_tour)
            new_giant_tour.remove(best_node)
            return self.remove_node(new_giant_tour)
        else:
            return giant_tour
                
            
        
    def get_giant_tour(self, individual):
        '''
        scan from left to right to extract a giant tour
        '''
        giant_tour = []
        i = 0
        covering_set = set()
        
        while True:
    #         print i, individual
            node_id = individual[i]
            i += 1
            # check if node belong to obligatory nodes
            if self.obligatory_nodes.issuperset(set([node_id])):
                giant_tour.append(node_id)
                continue
            
            covered_customers = self.get_set_of_customers_covered_by(node_id)
            
            if covered_customers.issubset(covering_set):
                continue
            
            # update tour
            giant_tour.append(node_id)
            
            # update covering set
            covering_set = covering_set.union(covered_customers)
            
            if len(covering_set) == self.num_of_customers:
                break
        
        # append all remaining nodes in individual that also in obligatory nodes into tour
        for node_id in individual[i:]:
            if self.obligatory_nodes.issuperset(set([node_id])):
                giant_tour.append(node_id)
                
        giant_tour = self.remove_node(giant_tour)
                
        individual.giant_tour = giant_tour
        
        return giant_tour
    
    def calculate_tours_cost(self, tours, job):
        '''
        calculate cost of a solution with explain detail
        '''
        f = open('cal_tours_cost.' + str(job), 'w')
        f.write(str(tours) +'\n')
        
        cost = 0
        for tour in tours:
            full_tour = [0] + tour + [0]
            for node1, node2 in zip(full_tour[:-1], full_tour[1:]):
                distance = self.nodes[node1].cost_dict[node2]
                
                line = '%s %s %s\n' %(node1, node2, distance)
                f.write(line)
                
                cost += distance
                
        f.write(str(cost))
        f.close()
        
    def export_gmctp(self):
        '''
        export generalized m-ctp
        '''
        # make new file name
#         t = self.name.split('.')[0]
#         file_name = "%s-%d.ctp" %(t, max_tour_length_type)
        file_name = self.name
        
        # generate covering constraint
        # how many nodes cover each customer
        cover_count = {}
        for node in xrange(1, self.num_of_nodes+len(self.obligatory_nodes)+1):
            for c in self.nodes[node].cover_list:
                if cover_count.has_key(c):
                    cover_count[c]+=1
                else:
                    cover_count[c]=1
                    
        node_cover =[]
        for c in xrange(self.num_of_customers):
            t = random.randint(1, min(3,cover_count[c]))
            node_cover.append(t)
        
        lines = open(self.data_path).readlines()
        lines[0] = '%d %d %d %d %.2f \n' %(self.num_of_nodes, self.num_of_customers, 
                            len(self.obligatory_nodes)+1, 
                            self.max_nodes_per_route,
                            self.max_tour_length)
        lines.append(' '.join(str(v) for v in node_cover))
        
        open(join('data_gmctp2', file_name), 'w').writelines(lines)
        
            
class MCTPProblem(CTPProblem):
    def load_data(self, data_path):
        self.data_path = data_path
        self.name = basename(data_path)
        
        lines = open(data_path, 'r').readlines()
        
        xs = [x for x in lines[0].split()]
        self.num_of_nodes = int(xs[0])
        self.num_of_customers = int(xs[1])
        obligatory_node = int(xs[2])
        
        self.max_nodes_per_route=int(xs[3])
        self.max_tour_length = float(xs[4])
        
        
        if len(xs)>5:
            self.best_cost = float(xs[5])
        else:
            self.best_cost = 0
        
        self.obligatory_nodes = set(range(1,obligatory_node))
        
        # init    
        for l in xrange(self.num_of_customers):
            self.nodes_covering_customer[l]=set()

        # initialize nodes
        self.nodes = []
        for i in xrange(self.num_of_nodes + obligatory_node):
            node = CTPNode(id=i, visited_cost=0, coverage_demand=0)
            self.nodes.append(node)
            
        # load cost matrix
        i = 1
        line = lines[i]
        while not line.isspace():
            xs = line.split()
            id1, id2 = [int(x) for x in xs[:2]]
            distance = float(xs[-1])
            self.nodes[id1].cost_dict[id2] = distance
            self.nodes[id2].cost_dict[id1] = distance
            
            i += 1
            line = lines[i]
        
        # load covering matrix
        i += 1
        for line in lines[i:-1]:
            xs = [int(x) for x in line.split()]
            for i in xrange(self.num_of_customers):
                if xs[i+1] == 1:
                    self.nodes[xs[0]].cover_list.append(i)
                    self.nodes_covering_customer[i].update([xs[0]])
                    
class GMCTPProblem(CTPProblem):
    def load_data(self, data_path):
        self.data_path = data_path
        self.name = basename(data_path)
        
        lines = open(data_path, 'r').readlines()[1:]
        
        xs = [x for x in lines[0].split()]
        self.num_of_nodes = int(xs[0])
        self.num_of_customers = int(xs[1])
        obligatory_node = int(xs[2])
        
        self.max_nodes_per_route=int(xs[3])
        self.max_tour_length = float(xs[4])
        
        
        if len(xs)>5:
            self.best_cost = float(xs[5])
        else:
            self.best_cost = 0
        
        self.obligatory_nodes = set(range(1,obligatory_node))
        
        # init    
        for l in xrange(self.num_of_customers):
            self.nodes_covering_customer[l]=set()

        # initialize nodes
        self.nodes = []
        for i in xrange(self.num_of_nodes + obligatory_node):
            node = CTPNode(id=i, visited_cost=0, coverage_demand=0)
            self.nodes.append(node)
            
        # load cost matrix
        i = 1
        line = lines[i]
        while not line.isspace():
            xs = line.split()
            id1, id2 = [int(x) for x in xs[:2]]
            distance = float(xs[-1])
            self.nodes[id1].cost_dict[id2] = distance
            self.nodes[id2].cost_dict[id1] = distance
            
            i += 1
            line = lines[i]
        
        # load covering matrix
        i += 1
        for line in lines[i:-1]:
            xs = [int(x) for x in line.split()]
            for i in xrange(self.num_of_customers):
                if xs[i+1] == 1:
                    self.nodes[xs[0]].cover_list.append(i)
                    self.nodes_covering_customer[i].update([xs[0]])
        
        
        # load customer covering constraint
        self.customer_covering = [int(x) for x in lines[-1].split()]
        
    def is_giant_tour_satisfy_covering_constraint(self, giant_tour):
        
        # get covering set of all remaining nodes:
        covering_dict={}
        
        for node in giant_tour:
            # if it is a node in obligatory nodes, then jump to a next node
            if self.obligatory_nodes.issuperset(set([node])):
                continue
        
            for c in self.nodes[node].cover_list:
                if covering_dict.has_key(c):
                    covering_dict[c] += 1
                else:
                    covering_dict[c] = 1
                    
                
        if len(covering_dict) != self.num_of_customers:
            return False
        else:
            for c in xrange(self.num_of_customers):
                if covering_dict[c] < self.customer_covering[c]:
                    return False
        
        return True

    def is_tours_satisfy_covering_constraint(self, tours):
        
        giant_tour = self.concat(tours)
        return self.is_giant_tour_satisfy_covering_constraint(giant_tour)
    
        
    def export_to_file(self):
        ps = self.name.split('-')
        p = ps[0]
        max_length_type = int(ps[-1].split('.')[0])
        
        T = len(self.obligatory_nodes)+1
        N = T + self.num_of_nodes
                
        lines = []
        file_name = '%s-%d-%d-%d-%d.ctp' %(p, T, N, self.num_of_customers, self.max_nodes_per_route)
        lines.append(self.name + "\n")
        lines.append('%d %d %d %d %.2f\n' %(self.num_of_nodes, self.num_of_customers, T, self.max_nodes_per_route, self.max_tour_length))
        
        # write cost
        for i in xrange(N-1):
            for j in xrange(i+1, N):
#                 print i, j
                lines.append('%d %d %.2f\n' %(i, j, self.nodes[i].cost_dict[j]))
                
        lines.append('\n')
        # covering
        for i in xrange(T, N):
            line = [i] + [0]*self.num_of_customers
            for c in self.nodes[i].cover_list:
                line[c+1] = 1
            line = ' '.join(str(v) for v in line) + "\n"
            
            lines.append(line)
            
        # covering constraint
        line = ' '.join([str(v) for v in self.customer_covering])
        
        lines.append(line)
        
        open(join('data_gmctp_cv_full', file_name), 'w').writelines(lines)
         

    def convert_to_gmctp1(self):
        gmctp = GMCTPProblem(data_path="", max_tour_length=self.max_tour_length
                         , load_data_from_file=False)
        gmctp.name = self.name
        gmctp.num_of_customers = self.num_of_customers
        gmctp.customer_covering = deepcopy(self.customer_covering)
        gmctp.obligatory_nodes = deepcopy(self.obligatory_nodes)
        gmctp.max_nodes_per_route = self.max_nodes_per_route
        gmctp.max_tour_length = self.max_tour_length
        
        # copy depot
        depot = self.nodes[0].clone()
        depot.cost_dict.clear()
        gmctp.nodes.append(depot)

        id = 1
        nodes_copy_from_node = [[0]]
        for i in xrange(1, self.num_of_nodes + len(self.obligatory_nodes) + 1):
            if self.obligatory_nodes.issuperset(set([i])):
                node = self.nodes[i].clone()
                node.id = id
                gmctp.nodes.append(node)
                nodes_copy_from_node.append([id])

                id += 1
                continue
            
            num_of_copies = max([self.customer_covering[c] for c in self.nodes[i].cover_list])
            nodes_copy_from_node.append([])


            for _ in xrange(num_of_copies):
                node = self.nodes[i].clone()
                node.cost_dict.clear()
                node.id = id
                gmctp.nodes.append(node)
                nodes_copy_from_node[i].append(id)
                
                id += 1
        
        gmctp.num_of_nodes = len(gmctp.nodes)-len(gmctp.obligatory_nodes)-1
        
        # init    
        for l in xrange(self.num_of_customers):
            gmctp.nodes_covering_customer[l]=set()
        # cost matrix and cover list and nodes covering a customer
        n = self.num_of_nodes + len(self.obligatory_nodes)+1
        for i in xrange(n):
            copy_nodes_i = nodes_copy_from_node[i]
            
            # cost between nodes that are copied from one node
            for t in copy_nodes_i:
                for k in copy_nodes_i:
                    if t != k:
                        gmctp.nodes[t].cost_dict[k] = 0
            
            # cost from each copies with other copy from other nodes
            for j in xrange(n):
                if j == i:
                    continue
                copy_nodes_j = nodes_copy_from_node[j]
                
                cost = self.nodes[i].cost_dict[j] 
                
                for copy_node_i in copy_nodes_i:
                    # cost
                    for copy_node_j in copy_nodes_j:
                        gmctp.nodes[copy_node_i].cost_dict[copy_node_j] = cost
                    # nodes covering a customer
                    for c in gmctp.nodes[copy_node_i].cover_list:
                        gmctp.nodes_covering_customer[c].update([copy_node_i])
        
        gmctp.export_to_file()
            
if __name__ == '__main__':
    data_path = '/home/pta/projects/ctp/data_ctp/kroA-13-12-75-1.ctp'
    problem = CTPProblem(data_path=data_path)
#     problem.load_data(data_path)

    # build test split alg from prins' paper
    for i in xrange(6):
        node = CTPNode(0, visited_cost=5)
        if i == 5:
            node.visited_cost = 6
                        
        problem.nodes.append(node)
        
    #demand
    problem.nodes[1].load = 4
    problem.nodes[2].load = 3
    problem.nodes[3].load = 5
    problem.nodes[4].load = 1
    problem.nodes[5].load = 6
    
        
    problem.nodes[0].cost_dict[1] = 20
    problem.nodes[1].cost_dict[0] = 12
    
    problem.nodes[0].cost_dict[2] = 11
    problem.nodes[2].cost_dict[0] = 11
    
    problem.nodes[0].cost_dict[3] = 20
    problem.nodes[3].cost_dict[0] = 15
    
    problem.nodes[0].cost_dict[4] = 13
    problem.nodes[4].cost_dict[0] = 14

    problem.nodes[0].cost_dict[5] = 10
    problem.nodes[5].cost_dict[0] = 16

    problem.nodes[1].cost_dict[2] = 10
    problem.nodes[2].cost_dict[1] = 10

    problem.nodes[2].cost_dict[3] = 20
    problem.nodes[3].cost_dict[2] = 20

    problem.nodes[3].cost_dict[4] = 20
    problem.nodes[4].cost_dict[3] = 20
    
    problem.nodes[4].cost_dict[5] = 9
    problem.nodes[5].cost_dict[4] = 9
    
    giant_tour = [1,2,3,4,5]
    cost,p = problem.new_split(giant_tour)
    
    tour = problem.extract_tours(giant_tour, p)

    print cost
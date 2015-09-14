'''
Created on Aug 17, 2015

@author: pta
'''
from os.path import basename

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
        
        
class CTPProblem():
    def __init__(self, data_path, vehicle_capacity=100000):
        self.nodes = []
        self.num_of_vehicles = 1
        self.max_nodes_per_route=0
        self.obligatory_nodes = set()
        self.num_of_nodes = None 
        self.num_of_customers = None
        self.vehicle_capacity = vehicle_capacity
        self.best_cost = 0
        self.giant_tour_cost={}
        self.n_same_giant_tour = 0
        
        self.__load_data(data_path)
        
    def __load_data(self, data_path):
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
        
        self.obligatory_nodes = set(range(obligatory_node))
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
                    
    def get_set_of_customers_covered_by(self, node_id):
        '''
        get a set of customers that covered by a node (node_id)
        '''
        return set(self.nodes[node_id].cover_list)

if __name__ == '__main__':
    data_path = '/home/pta/projects/ctp/data_ctp/kroA-13-12-75-1.ctp'
    problem = CTPProblem()
    problem.load_data(data_path)
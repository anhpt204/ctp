'''
Generalized Covering Salesman Problem
'''
from problem import CTPProblem, CTPNode
from os.path import split, basename

class GCSPProblem(CTPProblem):
    def __init__(self, data_path, vehicle_capacity=100000):
        self.covering_freq = {}
        CTPProblem.__init__(self, data_path, vehicle_capacity)
        
    def load_data(self, data_path):        

        self.name = split(basename(data_path))[0]
        
        lines = open(data_path, 'r').readlines()
        
        xs = lines[0].split()
        
        self.num_of_nodes = int(xs[0])
        self.num_of_customers = int(xs[1])
        self.max_nodes_per_route = int(xs[2])
                
        # initialize nodes
        self.nodes = []
        for i in xrange(self.num_of_nodes):
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
        for k in xrange(self.num_of_nodes-1):
            line = lines[i+k]
            xs = [int(x) for x in line.split()]
            for j in xrange(self.num_of_customers):
                if xs[j+1] == 1:
                    self.nodes[xs[0]].cover_list.append(j)            
            
        # load covering constraint
        xs = [int(x) for x in lines[-1].split()]
        for i in xrange(self.num_of_customers):
            self.covering_freq[i] = xs[i]
            
            
            
                
                    
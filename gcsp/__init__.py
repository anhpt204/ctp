'''
Generalized Covering Salesman Problem
'''
from problem import CTPProblem, CTPNode

class GCSPProblem(CTPProblem):
    def __init__(self, data_path, vehicle_capacity=100000):
        self.covering_freq = {}
        CTPProblem.__init__(self, data_path, vehicle_capacity)
        
    def load_data(self, data_path):        
        
        lines = open(data_path, 'r').readlines()
        
        xs = lines[0].split()
        
        self.num_of_nodes = int(xs[0])
        self.num_of_customers = int(xs[1])
        self.max_nodes_per_route = int(xs[2])
        
        # initialize nodes
        self.nodes = []
        for i in xrange(self.num_of_nodes):
            node = CTPNode(id, visited_cost=0, coverage_demand=0)
            self.nodes.append(node)
        line_number = 1
        # load cost matrix
        for i in xrange(self.num_of_nodes-1):
            xs = lines[line_number].split()
            id1 = int(xs[0])
            j = 1
            for id2 in xrange(id1+1, self.num_of_nodes):
                distance = float(xs[j])
                
                self.nodes[id1].cost_dict[id2] = distance
                self.nodes[id2].cost_dict[id1] = distance

                j+=1
            line_number +=1
            
        # load covering matrix
        for i in xrange(self.num_of_nodes):
            xs = [int(x) for x in lines[line_number].split()]            
            self.nodes[xs[0]].cover_list = xs[1:]
            line_number+=1
            
            
        # load covering constraint
        xs = [int(x) for x in lines[-1].split()]
        for i in xrange(self.num_of_customers):
            self.covering_freq[i] = xs[i]
            
            
            
                
                    
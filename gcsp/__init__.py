'''
Generalized Covering Salesman Problem
'''
from problem import CTPProblem, CTPNode

class GCSPProblem(CTPProblem):
    def __init__(self):
        super(GCSPProblem, self).__init__()
        
    def load_data(self, data_path):
        
        lines = open(data_path, 'r').readlines()
        
        self.num_of_nodes = int(lines[0])
        
        
        self.obligatory_nodes = set(range(obligatory_node))
        # initialize nodes
        self.nodes = []
        for i in xrange(self.num_of_nodes + obligatory_node):
            node = CTPNode(id, visited_cost=0, coverage_demand=0)
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
                    
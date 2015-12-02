'''
Generalized Covering Salesman Problem
'''
from problem import CTPProblem, CTPNode
from os.path import split, basename

class GCSPProblem(CTPProblem):
    def __init__(self, data_path, max_tour_length=100000):
        # the number of nodes that cover a customer 
        self.covering_freq = {}
        
        # list of nodes that cover a customer
        self.nodes_covering_customer={}
        
        CTPProblem.__init__(self, data_path, max_tour_length)
        
    def load_data(self, data_path):        

        self.name = split(basename(data_path))[0]
        
        lines = open(data_path, 'r').readlines()
        
        xs = lines[0].split()
        
        self.num_of_nodes = int(xs[0])
        self.num_of_customers = int(xs[1])
        self.max_nodes_per_route = int(xs[2])
            
        # init    
        for l in xrange(self.num_of_customers):
            self.nodes_covering_customer[l]=set()
            
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
                    self.nodes_covering_customer[j].update([xs[0]])          
            
        # load covering constraint
        xs = [int(x) for x in lines[-1].split()]
        for i in xrange(self.num_of_customers):
            self.covering_freq[i] = xs[i]
            
    
############################################################
### For new version of CTP with constraint on the number nodes that cover a customer
#############################################################
#     def is_giant_tour_satisfy_covering_constraint(self, giant_tour):
#         covering_freq={}
#         for node in giant_tour:
#             covered_customers = self.get_set_of_customers_covered_by(node)
#             # update frequency
#             for cusId in covered_customers:
#                 if covering_freq.has_key(cusId):
#                     covering_freq[cusId]+=1
#                 else:
#                     covering_freq[cusId]=1
#                     
#         # check if this giant tour satisfies covering constaint
#         satisfy = False
#         if len(covering_freq) == self.num_of_customers:
#             satisfy=True
#             for cusId, freq in covering_freq.items():
#                 if freq < self.covering_freq[cusId]:
#                     satisfy = False
#                     break
#         if satisfy:
#             return True
#         
#         return False                                    
#         
#     def is_tours_satisfy_covering_constraint(self, tours):
#         covering_freq={}
#         for tour in tours:
#             for node in tour:
#                 covered_customers = self.get_set_of_customers_covered_by(node)
#                 # update frequency
#                 for cusId in covered_customers:
#                     if covering_freq.has_key(cusId):
#                         covering_freq[cusId]+=1
#                     else:
#                         covering_freq[cusId]=1
#                     
#         # check if this giant tour satisfies covering constaint
#         satisfy = False
#         if len(covering_freq) == self.num_of_customers:
#             satisfy=True
#             for cusId, freq in covering_freq.items():
#                 if freq < self.covering_freq[cusId]:
#                     satisfy = False
#                     break
#         if satisfy:
#             return True
#         
#         return False                                    
#         
#             
#     def get_giant_tour(self, individual):
#         '''
#         scan from left to right to extract a giant tour
#         '''
#         giant_tour = []
#         i = 0
#         covering_freq = {}
#         
#         while True:
#     #         print i, individual
#             node_id = individual[i]
#             i += 1
# #             # check if node belong to obligatory nodes
# #             if self.obligatory_nodes.issuperset(set([node_id])):
# #                 giant_tour.append(node_id)
# #                 continue
#             
#             covered_customers = self.get_set_of_customers_covered_by(node_id)
#             #update frequency each customer covered
#             for cusId in covered_customers:
#                 if covering_freq.has_key(cusId):
#                     covering_freq[cusId]+=1
#                 else:
#                     covering_freq[cusId]=1
#             
#             # update tour
#             giant_tour.append(node_id)
#             
#             # check if this giant tour satisfies covering constaint
#             satisfy = False
#             if len(covering_freq) == self.num_of_customers:
#                 satisfy=True
#                 for cusID, freq in covering_freq.items():
#                     if freq < self.covering_freq[cusID]:
#                         satisfy = False
#                         break
#             if satisfy:
#                 break                                    
#                 
#         giant_tour = self.remove_node(giant_tour)
#                 
#         individual.giant_tour = giant_tour
#         
#         return giant_tour
        
            
            
            
                
                    
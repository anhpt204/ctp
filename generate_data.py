'''
Created on Sep 23, 2015

Generate CTP data

@author: pta
'''
from math import sqrt
import operator
import random
from copy import deepcopy
from os.path import join, basename
import glob
from problem import CTPProblem, GMCTPProblem

# random.seed(1000)

nodes_customers=((50,50), (50,100), (100,100), (100,200), (200,200))
max_vertices_per_route = [4, 5, 6, 8]
max_neighbours = [7, 9, 11]

XY=xrange(0,500)

def gen_ctp_data_generalized(conf, data_file):
     
    random.seed(1000)
    
    #read data
    vertices =[]
    lines = open(data_file, 'r').readlines()
    for line in lines:
        xs = [int(x) for x in line.split()]
        vertices.append((xs[1], xs[2]))
        
#     v = random.sample(vertices, len)
    for len_v, len_w in conf:
         
        n = len_v + len_w
        lines = []
         
#         x_samples = random.sample(XY)
#         y_samples = random.sample(XY)
#          
#         vertices = [(x,y) for x,y in zip(x_samples, y_samples)]
         
        # set of nodes
#         v = random.sample(vertices, len_v)
        v = vertices[:len_v]
        #set of customers
#         w = list(vertices.difference(set(v)))
        w = vertices[len_v:]
        #write distance for each (i, j) in V
        for i in xrange(0,len_v-1):
            line = str(i)
            for j in xrange(i+1, len_v):
                #calculate euclidean distance
                d = sqrt((v[i][0] - v[j][0])**2 + (v[i][1]-v[j][1])**2)
                 
#                 line = line + ' %.2f' %(d)
                lines.append('%d %d %d\n' %(i, j, int(round(d))))
#             lines.append(line+'\n')
             
        # calculate fixed radius d = max(max1, max2)
        # generate list of dicts: distance from l in W to nodes k in V
        distances = []
        for l in xrange(len_w):
            cost_dict = {}
            for k in xrange(1, len_v): #ignore 0 for depot
                dist = sqrt((w[l][0]-v[k][0])**2 + (w[l][1]-v[k][1])**2)
                cost_dict[k]=dist
            distances.append(cost_dict)
        # get max1
        max1 = 0
        for k in xrange(1, len_v):
            min_dkl = 10**10
            for l in xrange(len_w):
                if distances[l][k] < min_dkl:
                    min_dkl=distances[l][k]
            if min_dkl > max1:
                max1=min_dkl
        # get max2
        c_kl=[]
        for cost_dict in distances:
            # get kl by sorting cost_dict by values and get second value
            cost_dict_sorted = sorted(cost_dict.items(), key=operator.itemgetter(1))
             
            c_kl.append(cost_dict_sorted[2][1])
        max2 = max(c_kl)
         
        # fixed radius
        d = max(max1, max2)
        d_ = 2*d
         
        customers_covered_freq = {}
        # write covered vertices
        lines.append('\n')
        for k in xrange(1, len_v):
            line = str(k)
            for l in xrange(len_w):
                cost_dict = distances[l]
                if cost_dict[k] <= d_ and random.random() <= 0.5:
                    line = line + ' 1'
                    
                    if customers_covered_freq.has_key(l):
                        customers_covered_freq[l] += 1
                    else:
                        customers_covered_freq[l] = 1
                        
                else:
                    line = line + ' 0'
            line = line + '\n'
            lines.append(line)
             
        # covered constraint
        lines.append('\n')
        line = ''
        for l in xrange(len_w):
            c = random.randint(1,min(3, customers_covered_freq[l]))
            line = line + ' ' + str(c)
        lines.append(line)
 
        for max_vertices in max_vertices_per_route:
            problem_name ='D-%d-%d-%d.ctp' %(len_v, len_w, max_vertices)
 
 
            out = open('/home/pta/git/ctp/data/'+problem_name, 'wb')
            out.write('%d %d %d\n' %(len_v, len_w, max_vertices))
 
            out.writelines(lines)
            out.close()
            
            
    
# def gen_ctp_data_generalized(rnd_seed):
#     
#     random.seed(rnd_seed)
# 
#     for len_v, len_w in nodes_customers:
#         
#         n = len_v + len_w
#         lines = []
#         
#         x_samples = random.sample(XY,n)
#         y_samples = random.sample(XY,n)
#         
#         vertices = [(x,y) for x,y in zip(x_samples, y_samples)]
#         
#         # set of nodes
#         v = vertices[:len_v]
#         #set of customers
#         w = vertices[len_v:]
#         
#         #write distance for each (i, j) in V
#         for i in xrange(0,len_v-1):
#             line = str(i)
#             for j in xrange(i+1, len_v):
#                 #calculate euclidean distance
#                 d = sqrt((v[i][0] - v[j][0])**2 + (v[i][1]-v[j][1])**2)
#                 
# #                 line = line + ' %.2f' %(d)
#                 lines.append('%d %d %d\n' %(i, j, int(d)))
# #             lines.append(line+'\n')
#             
#         # generate list of dicts: distance from k in V to nodes l in W
#         distances = []
#         # for each vertex k in V, k != 0
#         for k in xrange(1,len_v): #ignore 0 for depot
#             cost_dict = {}
#             #for each vertex l in W
#             for l in xrange(len_w): 
#                 # get distance between k and l
#                 dist = sqrt((w[l][0]-v[k][0])**2 + (w[l][1]-v[k][1])**2)
#                 cost_dict[l]=int(dist)
#             sorted_cost_dict = sorted(cost_dict.items(),key=operator.itemgetter(1))                
#             distances.append(sorted_cost_dict)        
#         lines.append('\n')
#         # write covered vertices
#         for max_neighbour in max_neighbours:
#             new_lines = deepcopy(lines)
#             
#             customer_covering_freq = {}
#             for k in xrange(1, len_v):
#                 line = str(k)
#                 # get list of customer covered by node k
# #                 print k, distances[k]
#                 customers_covered = distances[k-1][:max_neighbour]
#                 # update frequency of a customer covered
#                 customers_covered_keys =[]
#                 for l, d in customers_covered:
#                     customers_covered_keys.append(l)
#                     if customer_covering_freq.has_key(l):
#                         customer_covering_freq[l] += 1
#                     else:
#                         customer_covering_freq[l] = 1
#                         
#                 for l in xrange(len_w):
#                     if customers_covered_keys.count(l) == 1:
#                         line += ' %d' %(1)
#                     else:
#                         line += ' %d' %(0)
#                 line = line + '\n'
#                 new_lines.append(line)
# 
#             if len(customer_covering_freq) < len_w:
#                 continue
#                
#             # covered constraint
#             new_lines.append('\n')
#             line = ''
#             for l in xrange(len_w):
#                 c = random.randint(1,(min(3, customer_covering_freq[l])))
#                 line = line + ' ' + str(c)
#             new_lines.append(line)
#         
#             for max_vertices in max_vertices_per_route:
#                 problem_name ='g-%d-%d-%d-%d.%d.ctp' %(len_v, len_w, max_vertices, max_neighbour, rnd_seed)
# 
#                 out = open('/home/pta/git/ctp/data/'+problem_name, 'wb')
#                 out.write('%d %d %d %d\n' %(len_v, len_w, max_vertices, max_neighbour))
# 
#                 out.writelines(new_lines)
#                 out.close()
    
def gen_ctp_max_node_per_route():
    data_files = glob.glob(join('data_gmctp_cv_full', '*.ctp'))
    dir_out = 'data_gmctp2'
    max_nodes = [4,5,6,8]
    for file in data_files:
        lines = open(file).readlines()
        vs = lines[1].split()
        
        for max_node in max_nodes:
            ns = basename(file).split('-')
            ns[-1] = str(max_node) + '.ctp'
            file_name = '-'.join(ns)
            vs[3] = str(max_node)
            lines[1] = ' '.join(vs)
            
            open(join(dir_out, file_name), 'w').writelines(lines)
            
def gen_ctp_full_constraints():
    '''
    max node per route and max tour length
    '''
    data_files = glob.glob(join('data_gmctp_cv_full', '*.ctp'))
    dir_out = 'data_gmctp'
    max_nodes = [4,5,6,8]
    tour_length_types = [250, 500]
    
    for file in data_files:
        print file
#         file = 'data_gmctp_cv_full/A1-1-145-50-4.ctp'
        problem = GMCTPProblem(data_path=file)
        
        lines = open(file).readlines()
        vs = lines[1].split()        
        for max_node in max_nodes:
            ns = basename(file).split('-')
            ns[-1] = str(max_node)
            ns.append('')
            for tour_length_type in tour_length_types:
                ns[-1] = str(tour_length_type) + ".ctp"
                file_name = '-'.join(ns)
                
                vs[3] = str(max_node)
                
                n = problem.num_of_nodes + len(problem.obligatory_nodes) + 1
                cost_from_depot = [problem.nodes[0].cost_dict[node] for node in range(1, n)]
                max_cost_from_depot = max(cost_from_depot)#          
                
                max_tour_length = 2*max_cost_from_depot + tour_length_type        
                
                vs.insert(4, str(max_tour_length))
                del vs[5:]
                lines[1] = ' '.join(vs) + "\n"
            
                open(join(dir_out, file_name), 'w').writelines(lines)
            

if __name__ == '__main__':
    
#     gen_ctp_max_node_per_route()

    gen_ctp_full_constraints()
    
# #     for job in (1,2,3,4,5):
# #         gen_ctp_data_generalized(job)
#     data_file='/home/pta/git/ctp/tsplib/kroD100.tsp'
#     conf=((50,50), (25,75))
#     gen_ctp_data_generalized(conf, data_file)
    print 'DONE'
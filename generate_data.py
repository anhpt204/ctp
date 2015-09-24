'''
Created on Sep 23, 2015

Generate CTP data

@author: pta
'''
from math import sqrt
import operator
import random

# random.seed(1000)

len_vs = [100, 500]
len_ws = [1, 2, 3, 4, 5]
max_vertices_per_route = [4, 5, 6, 8]

def gen_ctp_data_fixed_radius():

    random.seed(1000)
        
    for len_v in len_vs:
        for t in len_ws:
            len_w = len_v*t
            n = len_v + len_w
            lines = []
            
            samples = xrange(0,n)
            x_samples = random.sample(samples, n)
            y_samples = random.sample(samples, n)
            
            vertices = [(x,y) for x,y in zip(x_samples, y_samples)]
            
            v = vertices[:len_v]
            w = vertices[len_v:]
            
            #write distance for each (i, j) in V
            for i in xrange(0,len_v-1):
                line = str(i)
                for j in xrange(i+1, len_v):
                    #calculate euclidean distance
                    d = sqrt((v[i][0] - v[j][0])**2 + (v[i][1]-v[j][1])**2)
                    
                    line = line + ' %.2f' %(d)
                    
                lines.append(line+'\n')
                
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
            
            # write covered vertices
            for k in xrange(1, len_v):
                line = str(k)
                for l in xrange(len_w):
                    cost_dict = distances[l]
                    if cost_dict[k] <= d:
                        line = line + ' %d' %(l)
                line = line + '\n'
                lines.append(line)
                
            # covered constraint
            line = ''
            for l in xrange(len_w):
                c = random.randint(1,4)
                line = line + ' ' + str(c)
            lines.append(line)
                
            for max_vertices in max_vertices_per_route:
                problem_name ='f-%d-%d-%d.ctp' %(len_v, len_w, max_vertices)


                out = open('/home/pta/git/ctp/data/f/'+problem_name, 'wb')
                out.write('%d %d %d\n' %(len_v, len_w, max_vertices))

                out.writelines(lines)
                out.close()
    
def gen_ctp_data_generalized():
    
    random.seed(1000)

    for len_v in len_vs:
        for t in len_ws:
            len_w = len_v*t
            n = len_v + len_w
            lines = []
            
            samples = xrange(0,n)
            x_samples = random.sample(samples, n)
            y_samples = random.sample(samples, n)
            
            vertices = [(x,y) for x,y in zip(x_samples, y_samples)]
            
            v = vertices[:len_v]
            w = vertices[len_v:]
            
            #write distance for each (i, j) in V
            for i in xrange(0,len_v-1):
                line = str(i)
                for j in xrange(i+1, len_v):
                    #calculate euclidean distance
                    d = sqrt((v[i][0] - v[j][0])**2 + (v[i][1]-v[j][1])**2)
                    
                    line = line + ' %.2f' %(d)
                    
                lines.append(line+'\n')
                
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
            
            
            # write covered vertices
            for k in xrange(1, len_v):
                line = str(k)
                for l in xrange(len_w):
                    cost_dict = distances[l]
                    if cost_dict[k] <= d_ and random.random() <= 0.5:
                        line = line + ' %d' %(l)
                line = line + '\n'
                lines.append(line)
                
            # covered constraint
            line = ''
            for l in xrange(len_w):
                c = random.randint(1,4)
                line = line + ' ' + str(c)
            lines.append(line)

            for max_vertices in max_vertices_per_route:
                problem_name ='g-%d-%d-%d.ctp' %(len_v, len_w, max_vertices)


                out = open('/home/pta/git/ctp/data/g/'+problem_name, 'wb')
                out.write('%d %d %d\n' %(len_v, len_w, max_vertices))

                out.writelines(lines)
                out.close()
    
if __name__ == '__main__':
    
    gen_ctp_data_fixed_radius()
    gen_ctp_data_generalized()
    
    print 'DONE'
'''
Created on Sep 8, 2015
@author: pta
'''
import random
from copy import deepcopy

def PMX(ind1, ind2):
    
    size = min(len(ind1), len(ind2))
    p1, p2 = [0]*(size+1), [0]*(size+1)

    # Initialize the position of each indices in the individuals
    for i in xrange(size):
        p1[ind1[i]] = i
        p2[ind2[i]] = i
    # Choose crossover points
#     cxpoint1 = random.randint(0, size)
#     cxpoint2 = random.randint(0, size - 1)
    # choose crossover points so that they are in giant tour
    cxpoint1_val = random.choice(ind1.giant_tour)
    cxpoint2_val = random.choice(ind2.giant_tour)
    
    cxpoint1 = ind1.index(cxpoint1_val)
    cxpoint2 = ind2.index(cxpoint2_val)
    
    
    if cxpoint2 >= cxpoint1 and cxpoint2 < size-1:
        cxpoint2 += 1
    else: # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1
    
    # Apply crossover between cx points
    for i in xrange(cxpoint1, cxpoint2):
        # Keep track of the selected values
        temp1 = ind1[i]
        temp2 = ind2[i]
        # Swap the matched value
        ind1[i], ind1[p1[temp2]] = temp2, temp1
        ind2[i], ind2[p2[temp1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]
    
    return ind1, ind2

def vrpPMX(ind1, ind2):
    '''
    PMX for VRP with solution is subset of nodes
    '''
    size=min(len(ind1), len(ind2))
    if size < 3:
        return ind1
    
    a,b=random.sample(xrange(size-1), 2)
    if a > b:
        a, b = b, a
    b = b+1
    
    # build mapping
    point_mapping = {}
    for i in xrange(a, b):
        if(ind1[i] == ind2[i]):
            continue
        
        point_mapping[ind1[i]]=ind2[i]                   
        
        # copy matched segment from ind1 to ind2
        ind2[i] = ind1[i]
        
    for i in xrange(len(ind2)):
        if i < a or i >= b:
            while point_mapping.has_key(ind2[i]):
                ind2[i] = point_mapping[ind2[i]]
                
    return ind2

def OX(ind1, ind2):
    size = min(len(ind1), len(ind2))
    a, b = random.sample(xrange(size), 2)
    if a > b:
        a, b = b, a

    holes1, holes2 = [True]*(size+1), [True]*(size+1)
    for i in range(size):
        if i < a or i > b:
            holes1[ind2[i]] = False
            holes2[ind1[i]] = False
    
    # We must keep the original values somewhere before scrambling everything
    temp1, temp2 = ind1, ind2
    k1 , k2 = b + 1, b + 1
    for i in range(size):
        if not holes1[temp1[(i + b + 1) % size]]:
            ind1[k1 % size] = temp1[(i + b + 1) % size]
            k1 += 1
        
        if not holes2[temp2[(i + b + 1) % size]]:
            ind2[k2 % size] = temp2[(i + b + 1) % size]
            k2 += 1
    
    # Swap the content between a and b (included)
    for i in range(a, b + 1):
        ind1[i], ind2[i] = ind2[i], ind1[i]
    
    return ind1, ind2

def scpOnePointCX(ind1, ind2):
    size = min(len(ind1), len(ind2))
    a = 0
    b=size-1
    
    for i in xrange(size):
        if ind1[i] != ind2[i]:
            a = i
            break
    for i in xrange(size-1, a, -1):
        if ind1[i] != ind2[i]:
            b = i
            break
            
    cxpoint = random.randint(a, b)
    
    ind1[cxpoint:], ind2[cxpoint:] = ind2[cxpoint:], ind1[cxpoint:]
    
    return ind1, ind2

def vrpOnePointCX(ind1, ind2):
    size = min(len(ind1), len(ind2))
    a = 0
    b=size-1
    
    for i in xrange(size):
        if ind1[i] != ind2[i]:
            a = i
            break
    for i in xrange(size-1, a, -1):
        if ind1[i] != ind2[i]:
            b = i
            break
            
    cxpoint = random.randint(a, b)
    
    ind1[cxpoint:], ind2[cxpoint:] = ind2[cxpoint:], ind1[cxpoint:]
    
    node_dict = {}
    for i in xrange(len(ind1)):
        if not node_dict.has_key(ind1[i]):
            node_dict[ind1[i]] = 1
        else:
            ind1[i] = 0
            
    while True:
        try:
            ind1.remove(0)
        except:
            break
        
            
    return ind1
'''
Created on Sep 16, 2015

@author: pta
'''
import csv
from os.path import splitext
from datetime import time, datetime

def crate_cost_table():

    f = open('out/ga_gt.csv', 'rb')
    lines = f.readlines()
    lines = sorted(lines)
    rows = []
    for line in lines:
        vs = line.split(';')
        # instance name
        vs[0]=splitext(vs[0])[0]
        
        vs[1:3] = [float(v) for v in vs[1:3]]
        if vs[2] < vs[1]:
            print '%s & %.2f & \\textbf{%.2f} \\\\' %(vs[0], vs[1], vs[2])
        elif vs[2] > vs[1]:
            print '%s & \\textbf{%.2f} & %.2f \\\\' %(vs[0], vs[1], vs[2])
        else:
            print '%s & %.2f & %.2f \\\\' %(vs[0], vs[1], vs[2])
            
#     for line in lines[2:98]:
#         vs = line.split()
#         vs[0] = splitext(vs[0])[0]
#         # 2,3
#         vs[3] =float(vs[3])
#         if vs[3] == 0:
#             vs[2] = '\\textbf{%s}' %(vs[2])
#             
#         # 4,5
#         vs[5] = float(vs[5])
#         if vs[5] == 0:
#             vs[4] = '\\textbf{%s}' %(vs[4])
#             
#         if vs[5] <0:
#             vs[4] = '{%s}*' %(vs[4])
#             
#         # 7 8
#         vs[8] = float(vs[8])
#         if vs[8] == 0:
#             vs[7] = '\\textbf{%s}' %(vs[7])
#         if vs[8] < 0:
#             vs[7] = '{%s}*' %(vs[7])
#             
#         # 10,11
#         vs[11] = float(vs[11])
#         if vs[11] == 0:
#             vs[10] = '\\textbf{%s}' %(vs[10])
#         if vs[11] < 0:
#             vs[10] = '{%s}*' %(vs[10])
#             
#         # 13,14
#         vs[14] = float(vs[14])
#         if vs[14] == 0:
#             vs[13] = '\\textbf{%s}' %(vs[13])
#         if vs[14] < 0:
#             vs[13] = '{%s}*' %(vs[13])
#             
#         # 16,17
#         vs[17] = float(vs[17])
#         if vs[17] == 0:
#             vs[16] = '\\textbf{%s}' %(vs[16])
#         if vs[17] < 0:
#             vs[16] = '{%s}*' %(vs[16])
#             
#         # 19,20
#         vs[20] = float(vs[20])
#         if vs[20] == 0:
#             vs[19] = '\\textbf{%s}' %(vs[19])
#         if vs[20] < 0:
#             vs[19] = '{%s}*' %(vs[19])
#         
#             
#             
#         row = '%s & %s & %s & %.2f & %s & %.2f & %s & %.2f & %s & %.2f & %s & %.2f & %s & %.2f \\\\' %(vs[0],vs[2], vs[4], vs[5], vs[7], vs[8], vs[10], vs[11], vs[13], vs[14], vs[16], vs[17], vs[19], vs[20])
        
        
#         print row
        
import time
        
def create_time_table():
    f = open('out/result.csv', 'rb')
    lines = f.readlines()
    
    rows = []
    
    for line in lines[2:98]:        
        vs = line.split()
        row = vs[0] = splitext(vs[0])[0]
        for i in xrange(6, len(vs), 3):
#             print vs[i]
#             xs = vs[i].split(':')
            t = datetime.strptime(vs[i], '%H:%M:%S.%f')
            row = row + '& %d' %(t.hour * 3600 + t.minute * 60 + t.second)
#             print row
            
        print row + '\\\\'
    
if __name__ == '__main__':
    
    crate_cost_table()

#     create_time_table()
    
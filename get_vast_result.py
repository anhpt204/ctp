'''
Created on Jan 4, 2016

@author: pta
'''
from os.path import join
import glob
from numpy import average
from datetime import datetime
out_dir = '/home/pta/Dropbox/ctp/out/no-ls4/mctp2_out'

desc_file = join(out_dir, 'convert_desc.txt')

def get_result_from_vast():
    desc_dict = {}
    lines = open(desc_file, 'r').readlines()
    for line in lines:
        vs = line.split()
        desc_dict[vs[0]] = vs[1]
    
    # read result
    result = []
    out_files = glob.glob1(out_dir, 'output.*')
    for out_file in out_files:
        lines = open(join(out_dir, out_file)).readlines()
        vs = lines[0].split()
        
        temp = lines[0][lines[0].find('[') + 1: lines[0].find(']')]
        xs = temp.split()
        ave_result = average([float(x) for x in xs])
        # get time
        run_time = datetime.strptime(lines[1], '%H:%M:%S.%f')
        run_second = run_time.hour*3600 + run_time.minute*60 + run_time.second
        
        result.append([desc_dict[vs[0]], float(vs[1]), float(vs[2]), ave_result, int(vs[3]), run_second])
        
    return result

def make_latex_table(result):
    for i in xrange(len(result)):
        row = result[i]
        if row[2] < row[1]:
            print '%s & %.2f & \\textbf{%.2f} & %.2f & %d & %.2f \\\\' %(row[0], row[1], row[2], row[3], row[4], row[5])
        elif row[2] > row[1]:
            print '%s & \\textbf{%.2f} & %.2f & %.2f & %d & %.2f \\\\' %(row[0], row[1], row[2], row[3], row[4], row[5])
        else:
            print '%s & %.2f & %.2f & %.2f & %d & %.2f \\\\' %(row[0], row[1], row[2], row[3], row[4], row[5])


if __name__ == '__main__':
    result = get_result_from_vast()
    result = sorted(result, key=lambda t:t[0])
    make_latex_table(result)
    
#     print result
    
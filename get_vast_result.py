'''
Created on Jan 6, 2016

@author: pta
'''
from os.path import join,splitext, isfile
import glob
from numpy import average
from datetime import datetime
from pytimeparse.timeparse import timeparse

out_dir = '/home/pta/Dropbox/ctp/out/mgctp1.0_out.adap.50'

hoang_out = '/home/pta/Dropbox/ctp/out/ELS/mgctp1.0'

desc_file = join(out_dir, 'convert_desc.txt')

def get_result_from_vast():
    desc_dict = {}
    lines = open(desc_file, 'r').readlines()
    for line in lines:
        vs = line.split()
        desc_dict[vs[0]] = splitext(vs[1])[0]

    # read result
    result = []
    out_files = glob.glob1(out_dir, 'output.*')
    for out_file in out_files:
        print out_file
        lines = open(join(out_dir, out_file)).readlines()
        vs = lines[-2].split()

        temp = lines[-2][lines[-2].find('[') + 1: lines[-2].find(']')]
        xs = temp.split()
        ave_result = average([float(x) for x in xs])
        # get time
        print lines[-1]

#        run_second = run_time.day*24 * 3600 + run_time.hour*3600 + run_time.minute*60 + run_time.second
        run_second = timeparse(lines[-1])
#        print run_second
	run_second = run_second/20

        result.append([desc_dict[vs[0]], 0,0,0, float(vs[2]), ave_result, int(vs[3]), run_second])

    return result

def get_result_from_hoang(result):
    for row in result:
        file = join(hoang_out, row[0]+".txt")
        if not isfile(file):
            continue

        lines = open(file).readlines()

        # duration
        duration = float(lines[-1].split('=')[1].split()[0].strip())
        # average
        average = float(lines[-2].split('=')[1].strip())
        # best solution
        best_solution = float(lines[-4].split('=')[1].strip())
        row[1:4] = best_solution, average, duration

def make_latex_table(result):
    for i in xrange(len(result)):
        row = result[i]
#        print row

        if row[4] < row[1]:
            if row[2] < row[5]:
                print '%s & %.2f & \\textbf{%.2f} & %.2f & \\textbf{%.2f} & %.2f & %d & %.2f \\\\' %(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            elif row[2] > row[5]:
                print '%s & %.2f & %.2f & %.2f & \\textbf{%.2f} & \\textbf{%.2f} & %d & %.2f \\\\' %(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            else:
                print '%s & %.2f & %.2f & %.2f & \\textbf{%.2f} & %.2f & %d & %.2f \\\\' %(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

        elif row[4] > row[1]:
            if row[2] < row[5]:
                print '%s & \\textbf{%.2f} & \\textbf{%.2f} & %.2f & %.2f & %.2f & %d & %.2f \\\\' %(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            elif row[2] > row[5]:
                print '%s & \\textbf{%.2f} & %.2f & %.2f & %.2f & \\textbf{%.2f} & %d & %.2f \\\\' %(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            else:
                print '%s & \\textbf{%.2f} & %.2f & %.2f & %.2f & %.2f & %d & %.2f \\\\' %(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        else:
            if row[2] < row[5]:
                print '%s & %.2f & \\textbf{%.2f} & %.2f & %.2f & %.2f & %d & %.2f \\\\' %(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            elif row[2] > row[5]:
                print '%s & %.2f & %.2f & %.2f & %.2f & \\textbf{%.2f} & %d & %.2f \\\\' %(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            else:
                print '%s & %.2f & %.2f & %.2f & %.2f & %.2f & %d & %.2f \\\\' %(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])


if __name__ == '__main__':
    result = get_result_from_vast()
    get_result_from_hoang(result)
    result = sorted(result, key=lambda t:t[0])
    make_latex_table(result)

#     print result

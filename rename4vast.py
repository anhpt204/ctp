'''
Created on Dec 22, 2015

@author: anhpt4
'''
from os.path import join
import glob 

dir_input = 'data_gmctp_cv'
dir_output = 'gmctp_vast_input'

files = glob.glob(join(dir_input, "*.ctp"))
for i, file in zip(xrange(1, len(files)+1), files):
    output_file = 'input.'+str(i)
    txt = open(file).read()
    open(join(dir_output, output_file),'w').write(txt)
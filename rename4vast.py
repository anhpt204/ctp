'''
Created on Dec 22, 2015

@author: anhpt4
'''
from os.path import join, basename
import glob 

dir_input = 'data_gmctp2'
dir_output = dir_input + '_vast'

files = glob.glob(join(dir_input, "*.ctp"))
files.sort()

convert_desc = []
for i, file in zip(xrange(1, len(files)+1), files):
    
    output_file = 'input.'+str(i)
#     print file, output_file
    convert_desc.append('%s %s\n' %(output_file, basename(file)))
                        
    txt = open(file).read()
    open(join(dir_output, output_file),'w').write(txt)
    
open(join(dir_output, 'convert_desc.txt'), 'w').writelines(convert_desc)
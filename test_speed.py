# run function Himmelblau 

#import math
from datetime import datetime
from os.path import join
import sys 

def run(input_file, output_file):
	start_time = datetime.now()

	N = 1000000000
	step = 12.0/N

	for i in xrange(N):
		x = -6 + i * step
		y = 6 - i * step
	
		f = 200 - (x*x + y - 11)**2 - (x + y**2-7)**2
		#print f

	end_time = datetime.now()
	duration = end_time - start_time
	open(join('test_speed', output_file), 'w').write(str(duration))

if __name__ == '__main__':
	run(sys.argv[1], sys.argv[2])

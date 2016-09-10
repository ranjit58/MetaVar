#! /bin/python

# command line : take a multi-sample vcf file and the names or positions of the sample files                             
  # allow for a command line option to list the names and positions of the sample file (so don't have to open to look)   
  # configuration file to list files from same subject                                                                   
# Take an initial time vcf and any number of vcf files from times > initial time                                         
# Extract the columns with the sample files                                                                              
# Raster through rows to grab any row with 1 : 0 or 0 : 1 (nothing with a . and not 1 : 1)                               
                                                                                                                          
# if not being passed directly to the next script, then create files with the data                                       
# otherwise just pass as variables to the next script

import argparse
import csv
import pdb
import sys

__author__="Brody DeSilva and Ranjit Kumar"
__email__="bdesilva@uab.edu, rkumar@uab.edu"

def print_samples(rows, offset):
	"This definition will print out the samples in a provided multi-sample vcf, given the row of the file.\n"
	for col in rows[offset + 1:-1]:
		print(str(rows.index(col) - offset) + '.\t' + col + '\t')
	return

parser = argparse.ArgumentParser(description="""Extract named samples from a Multi-Sample VCF file and output as a 2 column
vcf file.""")
parser.add_argument('multi',help="""Specify a multi-sample vcf file for reading and separating individual samples.""")
parser.add_argument('t_init',help="""Specify the name of the initial time vcf sample in the multi-sample vcf file.""")
parser.add_argument('t_final',help="""Specify the name of the second time vcf sample in the multi-sample vcf file.""")
parser.add_argument('-q', '--query',help="""Query the sample names of a provided multi-sample vcf
file.""",action='store_true')
parser.add_argument('-v', '--verbose',help="""Verbose mode will output additional information about how the program
	runs.""",action='store_true')
args = parser.parse_args()

if args.verbose:
	import time
	timein = time.time()

# logic to determine if is positional or based on the name
try:
	int(args.t_init)
	isposition = True
except ValueError:
	isposition = False

try:
	int(args.t_final)
	if not isposition:
		print('Enter either only position or only sample name as the command line parameter.\n')
		sys.exit()
except ValueError:
	if isposition:
		print('Enter either only position or only sample name as the command line parameter.\n')
		sys.exit()

init_flag = 0
final_flag = 0

# read each line
# find the sample line
# find the correct samples -> get the column numbers
# read in descriptor and sample columns

with open(args.multi) as f,  open('output.txt', 'w+') as out:
	multi  = csv.reader(f, delimiter="\t")
	header_offset = 8 # the number of columns until the first sample
	for row in multi:
		if row[0][1] != '#':
			# column 9 starts the samples
			# compare the samples to the sample data
			if init_flag == 0 and final_flag == 0:
					for header in row:
						if not isposition and header == args.t_init:
							init_col = row.index(header)
							init_flag = 1
						elif isposition:
							if row.index(header) - header_offset == int(args.t_init):
								init_col = row.index(header)
								init_flag = 1
						if not isposition and header == args.t_final:
							final_col = row.index(header)
							final_flag = 1
						elif isposition:
							if row.index(header) - header_offset == int(args.t_final):
								final_col = row.index(header)
								final_flag = 1
					if init_flag == 0 or final_flag == 0:
						print('Input a valid ID for the initial sample and the final sample.\n')
						print_samples(row, header_offset)
						sys.exit()
					
					for col in row[0:header_offset]:
						out.write(col + '\t')
					out.write(row[init_col] + '\t' + row[final_col] + '\n')
			else:
				for col in row[0:header_offset]:
					out.write(col + '\t')
				out.write(row[init_col] + '\t' + row[final_col] + '\n')

if args.verbose:
	timeout = time.time()
	elapse = timeout-timein
	print('Elapse time in seconds:\t' + str(elapse) + '.\n')

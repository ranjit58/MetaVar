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
try:
	# if running as a pipeline, will have a main function call
	from __main__ import pipeline_flag, pair, vcf, inter
except ImportError:
	# if running as a script
	pipeline_flag = 0

__author__="Brody DeSilva and Ranjit Kumar"
__email__="bdesilva@uab.edu, rkumar@uab.edu"

def print_extracted(data, out, headers, names):
	"This definition will print out the samples in a provided multi-sample vcf, given the row of the file.\n"
	out.write('#' + headers[0][1] + '\t' + names[0] + '\t' + names[1] + '\n')
	for sub in data:
		out.write(str(sub[0]) + '\t' + str(sub[1]) + '\t' + str(sub[2]) + '\n')
	return
def print_pairwise(data, out, headers):
	for el in headers:
		out.write(el + '\t')
	out.write('\n')
	for row in data:
		for sub in row:
			out.write(str(sub) + '\t')
		out.write('\n')
	return

if not pipeline_flag:
	parser = argparse.ArgumentParser(description="""Extract named samples from a Multi-Sample VCF file and output as a 2 column
	vcf file.""")
	parser.add_argument('multi',help="""Specify a multi-sample vcf file for reading and separating individual samples.""")
	parser.add_argument('t_init',help="""Specify the name of the initial time vcf sample in the multi-sample vcf file.""")
	parser.add_argument('t_final',help="""Specify the name of the second time vcf sample in the multi-sample vcf file.""")
	parser.add_argument('-q', '--query',help="""Query the sample names of a provided multi-sample vcf file.""",action='store_true')
	parser.add_argument('-v', '--verbose',help="""Verbose mode will output additional information about how the program
		runs.""",action='store_true')
	parser.add_argument('-o', '--output',help="""Specify the name of the output file, otherwise it will be the sample names.""")
	args = parser.parse_args()
	
	names = [args.t_init, args.t_final] # assume are names not positions
	vcf = args.multi
	output = args.output
	if args.verbose:
		import time
		timein = time.time()
else:
	names = [pair[0], pair[1]] # assume are names not positions
	output = None

# logic to determine if is positional or based on the name
try:
	int(names[0])
	isposition = True
except ValueError:
	isposition = False

try:
	int(names[1])
	if not isposition:
		print('Enter either only position or only sample name as the command line parameter.\n')
		sys.exit()
except ValueError:
	if isposition:
		print('Enter either only position or only sample name as the command line parameter.\n')
		sys.exit()

output_name = list()

# get output names
if output is None:
	output_name.append(names[0] + '_' + names[1] + '.txt') # get pairwise vcf
	output_name.append(output_name[0] + '.diff') # extracted
else:
	output_name.append(output)
	output_name.append(output + '.diff')

# read in data
with open(vcf) as f:
	vcf  = list(csv.reader(f, delimiter="\t"))
	headers = [row for row in vcf if row[0] == "#CHROM"]
	headers = headers[0] # remove outer list
	if not isposition:
		try:
			pos = [headers.index(el) for el in names]
		except ValueError:
			print('Sample names cannot be found.\nHere is a list of valid headers found:\n')
			print(headers)
			sys.exit()
	else:
		if int(names[0]) - 1 in range(len(headers)) and int(names[1]) - 1 in range(len(headers)):
			pos = [int(names[0]) - 1, int(names[1]) -1]
		else:
			print('The position was out of range.\nHere is a list of valid sample column values:\    n')
			print([el + 1 for el in range(len(headers))])
			sys.exit()
	if inter:
		with open(output_name[0], 'w+') as gpw:
			data = [[row[0:8], row[pos[0]], row[pos[1]]] for row in vcf if row[0][0] != '#']
			print_pairwise(data, gpw, headers[0:8] + names)

	# get the col info and position number
	data = [[row[pos[0]], row[pos[1]], row[1]] for row in vcf if row[0][0] != "#" if row[pos[0]][0] is '1' or row[pos[1]][0] is '1']
	# filter data
	data = [[pair[0], pair[1], pair[2]] for pair in data if pair[0][0] is not '.' and pair[1][0] is not '.']
	# remove double positives
	data = [[pair[0], pair[1], pair[2]] for pair in data if bool(pair[0][0] is '1') != bool(pair[1][0] is '1')]
	
	# rearrange, format, and print
	temp = [[int(pair[2]), 1, 0] for pair in data if pair[0][0] is '1']
	temp2 = [[int(pair[2]), 0, 1] for pair in data if pair[0][0] is '0']
	data = temp + temp2
	data.sort()
	if inter:
		with open(output_name[1], 'w+') as ext:
			print_extracted(data, ext, headers, names)

if not pipeline_flag:
	if isposition and args.output is None:
		# rename the file to the correct default name
		import os
		output_name_fix = init_change_name + '_' + final_change_name + '.txt'
		os.rename(output_name, output_name_fix) 
	if args.verbose:
		timeout = time.time()
		elapse = timeout-timein
		print('Elapse time in seconds:\t' + str(elapse) + '.\n')
		out.write(row[init_col] + '\t' + row[final_col] + '\n')

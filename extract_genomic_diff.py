#! /bin/python

# Input: the output of the get_paired_vcf.py file
# TO-DO: identify the differences and write to a new file 

import argparse
import csv
import sys
import pdb

def format_row(row):
	return '%s' % '\t'.join(map(str, row)) + '\n'


# argparse
parser = argparse.ArgumentParser(description="""Find the SNP differences between the two samples provided in the
intermediate multi-sample vcf file. Only look for the combinations: 1 0 or 0 1 (where 1 indicates a SNP and 0 indicates
no SNP).""")
parser.add_argument('input',help="""Specify a multi-sample vcf file with 2 linked samples (ex: time separated from the
same donor).""")
parser.add_argument('-p', '--position',help="""If the samples are not the last 2 columns of the vcf file, indicate the
column number (from left to right) of the first vcf sample (this will assume that the second vcf file is directly
following the first). Or specify the first vcf sample column number and the second vcf sample column
number.""",nargs='+')
parser.add_argument('-o', '--output', help="""Specify the output file name or path for saving.""")
parser.add_argument('-v', '--verbose',help="""See additional output about how the script is running.""",
action='store_true')

args = parser.parse_args()

if args.verbose:
	import time
	timein = time.time()

first_flag = False # first time through flag
if args.output is None:
	new_file = args.input + '.diff'
else:
	new_file = args.output

zero_based = 1 # to ameliorate the zero-based and one-based counting of a user v. python

# get the sample column position
if args.position is not None:
	if len(args.position) > 2:
		sys.exit('Input only 2 sample positions.\n')
	elif len(args.position) == 2:
		p_one = int(args.position[0]) - zero_based
		p_two = int(args.position[1]) - zero_based
		first_flag = True
	elif len(args.position) == 1:
		p_one = int(args.position[0]) - zero_based
		p_two = p_one + 1
		first_flag = True

count = 0
# open file and write to new file
with open(args.input) as f, open(new_file, 'w+') as out:
	multi = csv.reader(f, delimiter="\t")
	for row in multi:
		# get the sample position
		if not first_flag and args.position is None: # this way only executes check to true or false each iteration
			p_two = len(row) - 1
			p_one = p_two - 1
			first_flag = True
			out.write(format_row(row))
			count = 1
			continue # skip the header row
		if count == 0:
			out.write(format_row(row))
			count = 1
			continue
		# check the two positions
		# print the positions to file
		if row[p_one][0] == '.' or row[p_two][0] == '.':
			# if is any combination with '.' (meaning no information)
			continue
		elif int(row[p_one][0]) == 1 and int(row[p_two][0]) == 0:
			out.write(format_row(row))
		elif int(row[p_one][0]) == 0 and int(row[p_two][0]) == 1:
			out.write(format_row(row))
		else:
			# either 1 and 1 or 0 and 0
			continue
# the final 2 columns are for comparison

if args.verbose:
	timeout = time.time()
	elapse = timeout-timein
	print('Elapse time in seconds:\t' + str(elapse) + '.\n')

#! /bin/python

# Take input from the gff file and the differenced dual-sample linked vcf file and identify where in the gff genes, the
# SNP differences lie

import argparse
import csv
import sys
import pdb

__author__="Brody DeSilva, Ranjit Kumar"
__email__="bdesilva@uab.edu, rkumar@uab.edu"

# argparse
parser = argparse.ArgumentParser(description="""Input a dual-sample linked vcf file and a gff file. Find where the SNP
differences lie in the genes of the GFF file and output in a table format.""")
parser.add_argument('dual',help="""Specify a dual-sample vcf file for reading and pulling SNP bp locations.""")
parser.add_argument('gene',help="""Specify a gff file or a bed file for reading and pulling gene information.""")
parser.add_argument('-c','--column',help="""Specify the column number of the base pair locations for the SNP
changes.""", type=int)
parser.add_argument('-p','--position',help="""If the samples are not the last 2 columns of the vcf file, indicate the 
column number (from left to right) of the first vcf sample (this will assume that the second vcf file is directly        
following the first). Or specify the first vcf sample column number and the second vcf sample column                     
number.""",nargs='+', type=int)                                                                                         
parser.add_argument('-v','--verbose',help="""Verbose mode will output additional information about the program
execution.""", action='store_true')
parser.add_argument('-o','--output',help="""Specify the name of the output file.""")
args = parser.parse_args()

if args.verbose:
	import time
	timein = time.time()

zero_based = 1

if args.column is not None:
	bpc = args.column # base pair column

# get the sample column position
if args.position is not None:
	if len(args.position) > 2:
		sys.exit('Input only 2 sample positions.\n')
	elif len(args.position) == 2:
		p_one = args.position[0] - zero_based
		p_two = args.position[1] - zero_based
		first_flag = True
	elif len(args.position) == 1:
		p_one = args.position[0] - zero_based
		p_two = p_one + 1
		first_flag = True

if args.output is None:
	new_file = args.dual + '.tbl'
else:
	new_file = args.output

genes = []
gene_count = []
gene_info = []

# open the vcf and gff files or 8 column bed file
# columns 1, 2, 3, 7 from bed
# columns   from gff
with open(args.dual) as d, open(args.gff) as g, open(new_file) as out:
	dual = csv.reader(d, '\t')
	gene = csv.reader(g, '\t')
	for d_row in dual:
		# check for the 3rd (zero-based) column if is gene
		# check if the dual bp is inside the range of the gene
		for g_row in gene: # can make this quicker by only checking until a gene is inside region then next is outside
			# check for each one
			pdb.set_trace()
			if d_row[3][0:3] == 'gene':
				# check the ranges
				if d_row[1] < g_row[1] and d_row[2] > g_row[1]:
					# inside the range
					# put into an output table
					if genes.index(d_row[3]): # if gene already exists, then increment the count
						gene_count[genes.index(d_row[3])] += 1
					else: # otherwise append the gene and increment from 0
						genes.append(d_row[3])
						gene_count.append(1)
						gene_info.append(g_row[7])
			
			# 1 and 7 from dual


# either open each file and read in all the data needed or keep both files open as checking (first sounds better)









if args.verbose:
	elapse = timeout-time.time()
	print('Elapse time in seconds:\t' + str(elapse) + '.\n')

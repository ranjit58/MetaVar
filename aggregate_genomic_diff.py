#! /bin/python

# Take input from the gff file and the differenced dual-sample linked vcf file and identify where in the gff genes, the
# SNP differences lie

import argparse
import csv
import sys
import pdb

__author__="Brody DeSilva, Ranjit Kumar"
__email__="bdesilva@uab.edu, rkumar@uab.edu"

# gene class
# can always use Gene class with dictionary of name to access the gene
class Gene:
	"""A class for carrying gene information"""
	def __init__(self, name, count, info, bounds):
		self.name = name
		self.count = count
		self.info = info
		self.bounds = bounds
		self.snp = []

	def link(self, snp):
		self.snp.append(snp)

def genePresent(genes, name):
	"""genePresent(genes, name) takes a list of Gene objects and a name, then searches the names of the object for the specified object"""
	for gene in genes:
		if gene.name == name:
			return 1
		else:
			return 0
	

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
gene_bounds = list()
snp_loc = []
g_count = 0
d_count = 0
first_flag = 0

# open the vcf and gff files or 8 column bed file
# columns 1, 2, 3, 7 from bed
# columns   from gff
with open(args.dual) as d, open(args.gene) as g:
	dual = list(csv.reader(d, delimiter="\t"))
	gene = list(csv.reader(g, delimiter="\t"))

# grab the data
for d_row in dual:
	if first_flag == 0:
		first_flag = 1
		continue
	d_count += 1
	if d_count == 4:
		pdb.set_trace()
	# check for the 3rd (zero-based) column if is gene
	# check if the dual bp is inside the range of the gene
	for g_row in gene:
		for i in range(0, g_count): # assumes each file is ordered
			continue # basically since ordered start off where left off
		g_count += 1
		# check for each one
		if g_row[3][0:4] == "gene":
			# check the ranges
			if int(d_row[1]) >= int(g_row[1]) and int(d_row[1]) <= int(g_row[2]):
				# inside the range
				try:
					pdb.set_trace()
					genes.index(g_row[3]) # if gene already exists, then increment the count
					gene_count[genes.index(g_row[3])] += 1
					snp_loc.append(d_row[1])
					break
				except ValueError: # otherwise append the gene and increment from 0
					pdb.set_trace()
					genes.append(g_row[3])
					gene_count.append(1)
					gene_info.append(g_row[7])
					gene_bounds.append([int(g_row[1]), int(g_row[2])])
					snp_loc.append(d_row[1])
					break
		# 1 and 7 from dual




with open(new_file, 'w+') as out:
	pass
	# output the information
	# want to save the gene start and end, gene hit count, gene information, SNP location






pdb.set_trace()


if args.verbose:
	elapse = timeout-time.time()
	print('Elapse time in seconds:\t' + str(elapse) + '.\n')

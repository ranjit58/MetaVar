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
		self.snp = list()
		self.genome = []

	def link(self, snp):
		self.snp.append(snp)
	def genomeBound(self, bounds):
		self.genome = bounds

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

genes = dict()
first_flag = 0
g_count = 0
d_count = 0
# open the vcf and gff files or 8 column bed file
# columns 1, 2, 3, 7 from bed
# if bed, then set the numbers equal to the bed columns

# columns   from gff
# if gff, then set the numbers equal to the gff columns

with open(args.dual) as d, open(args.gene) as g:
	dual = list(csv.reader(d, delimiter="\t"))
	gene = list(csv.reader(g, delimiter="\t"))

# grab the data
for d_row in dual:
	g_count2 = g_count
	if first_flag == 0:
		first_flag = 1
		continue
	d_count += 1
	if args.verbose:
		t1 = time.time()
	snp_loc = d_row[1]

	if d_count == 16:
		pass
	# check for the 3rd (zero-based) column if is gene
	# check if the dual bp is inside the range of the gene
	while True:
		g_row = gene[g_count]
#		for i in range(0, g_count): # assumes each file is ordered
#			continue # basically since ordered start off where left off
		g_count += 1
		# check for each one
		if g_row[3][0:4] == "gene":
			# check the ranges
			if int(d_row[1]) >= int(g_row[1]) and int(d_row[1]) <= int(g_row[2]):
				name = g_row[3]
				count = 1
				info = g_row[7]
				bounds = [int(g_row[1]), int(g_row[2])]

				# inside the range
				try:
					genes[name].count += 1
					genes[name].link(snp_loc)
					if args.verbose:
						pass
						#print(str(time.time()-t1) + '\t' + str(g_count - g_count2))
					g_count += -1
					break
				except KeyError:
					genes[name] = Gene(name, count, info, bounds)
					genes[name].link(snp_loc)
					if args.verbose:
						pass
						#print(str(time.time()-t1) + '\t' + str(g_count - g_count2))
					g_count += -1
					break
		if g_count >= len(gene): # not all snps map to a gene
			if args.verbose:
				print('SNP\t' + str(d_row[1]) + '\tis not mapped to any gene.')
			g_count = g_count2
			break
		# 1 and 7 from dual




with open(new_file, 'w+') as out:
	for gene in genes:
		out.write(genes[gene].name + '\t' + str(genes[gene].count) + '\t' +
		str(genes[gene].bounds[0]) + ',' + str(genes[gene].bounds[1]) + '\t')
		firstsnp = True
		for snp in genes[gene].snp:
			if firstsnp:
				out.write(snp)
				firstsnp = False
			else:
				out.write(',' + snp)
		out.write('\t' + genes[gene].info + '\n')
	# output the information
	# want to save the gene start and end, gene hit count, gene information, SNP location

if args.verbose:
	elapse = time.time() - timein
	print('Elapse time in seconds:\t' + str(elapse) + '.\n')

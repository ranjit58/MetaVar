#! /bin/python

# Read in output of the previous script

# POS is column 1 (zero-based)
# Identify if ref or sample has SNP
# record 1 for has SNP and 0 for no SNP


import pandas as pd
import numpy as np
import argparse
import sys
import pdb

def inRange(bounds, num):
	if bounds[0] <= num <= bounds[1]:
		return True
	else:
		return False

def incrementSamples(g, f, gene, pos):
	sample = f.iloc[pos][f.iloc[pos] == 1].index
	for i in range(0, len(sample)):
		s = sample[i]
		g_ind = g.index[gene]
		g_v = g.loc[g_ind, s]
		g.set_value(g_ind, s, g_v + 1)

parser = argparse.ArgumentParser(description="""""")
parser.add_argument('file',type=argparse.FileType('r'),help="""Input a pairwise table file for reading.""")
parser.add_argument('gene',type=argparse.FileType('r'),help="""This is a gff file.""")
parser.add_argument('-b','--bed',help="""If using an 8 column bed file, specify with this
argument.""",action='store_true')
parser.add_argument('-v','--verbose',help="""Displays verbose output.""",action='store_true')
args = parser.parse_args()

if args.bed:
	g_cols = [1,2,3]
	in_col = 2
else: # gff
	g_cols = [2,3,4]
	in_col = 0

# read in the gene file
# g = pd.read_csv(args.gene, delimiter='\t', index_col=2, skiprows=3, names=range(0,3), usecols=g_cols)
g = pd.read_csv(args.gene, delimiter='\t', index_col=in_col, comment='#', names=["gene","start","stop"], usecols=g_cols, converters={"start":int, "stop":int})
g = g[g.index.str[0:4] == 'gene']

# read in the file as a pd dataframe
f = pd.read_csv(args.file, delimiter='\t', index_col=0, dtype=np.float64, na_values='.')
f = f.iloc[:, 0:-1]

# add the column names in f to g
for col in f.columns:
	g.loc[:, col] = 0

# do merging of the snps into the genes
# implement the counting that assumes ordered SNPs in terms of position
gene = 0
g_count = 0

for pos in  range(0, len(f.index)):
	g_count = gene
	while True: # while loop so can access the index
		gene += 1
		#gene = range(g_count, len(g.index))
		bounds = [g.iloc[gene][0], g.iloc[gene][1]]
		if inRange(bounds, f.index[pos]):
			incrementSamples(g, f, gene, pos)
			gene -= 1 # deal with the next SNP being in the same gene
			break
		elif gene == len(g.index) - 1:
			if args.verbose:
				print('SNP\t' + str(pos) + '\tat position:\t'  + str(f.index[pos]) + '\tis not in any gene.')
			gene = g_count - 1 # since has run through the entire list, reset to previous found gene
			break

g.loc[:, 'Avg'] = g[range(2, len(g.columns))].mean(axis=1)
out = args.file.name + '.comb'
g.drop(['start', 'stop'], axis=1, inplace=True)
g = g[(g.T != 0).any()]
g.to_csv(path_or_buf=out, sep='\t', na_rep='.')


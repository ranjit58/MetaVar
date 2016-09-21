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

parser = argparse.ArgumentParser(description="""""")
parser.add_argument('file',type=argparse.FileType('r'),help="""Input a pairwise table file for reading.""")
parser.add_argument('gene',type=argparse.FileType('r'),help="""This is either a 8 column bed file or a gff file.""")
args = parser.parse_args()

bed = True
if bed:
	num_cols = 8
	g_cols = [2,3,4]
else: # gff
	num_cols = 9

# read in the gene file
# g = pd.read_csv(args.gene, delimiter='\t', index_col=2, skiprows=3, names=range(0,3), usecols=g_cols)
g = pd.read_csv(args.gene, delimiter='\t', index_col=0, comment='#', names=["gene","start","stop"], usecols=g_cols,
converters={"start":int, "stop":int})
g = g[g.index.str[0:4] == 'gene']

# read in the file as a pd dataframe
f = pd.read_csv(args.file, delimiter='\t', index_col=0, dtype=np.float64, na_values='.')
f = f.iloc[:, 0:-1]

# add the column names in f to g
for col in f.columns:
	g.loc[:, col] = 0
g.loc[:, 'Avg'] = 0

# do merging of the snps into the genes
# implement the counting that assumes ordered SNPs in terms of position
for pos in  range(0, len(f.index)):
	for gene in range(0, len(g.index)):
		bounds = [g.iloc[gene][0], g.iloc[gene][1]]
		if inRange(bounds, f.index[pos]):
			sample = f.iloc[0][f.iloc[0] == 1].index[0]
			g_ind = g.index[gene]
			g_v = g.loc[g_ind, sample]
			g.set_value(g_ind, sample, g_v + 1)
			break
		elif gene == len(g.index) - 1:
			print('The SNP at position:\t' + str(f.index[pos]) + '\tis not in any gene.\n')
pdb.set_trace()	

files.append(pd.read_csv(args.file[csv], delimiter='\t', index_col=0))

combined = pd.concat([combined, combined.sum(axis=1, skipna=True)], axis=1)
combined.columns.values[-1] = 'Sum'
pdb.set_trace()





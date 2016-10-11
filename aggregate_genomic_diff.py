#! /bin/python
# Takes differenced pairwise samples and combines them into a table format
# Does not need to preserve the bp changes, only an indication of change or no change
# Table design: coordinate|annotation|1|2|3|4|Sum (samples 1, 2, 3, 4)

# POS is column 1 (zero-based)
# Identify if ref or sample has SNP
# record 1 for has SNP and 0 for no SNP

import pandas as pd
import numpy as np
import argparse
import sys
import pdb
import time

parser = argparse.ArgumentParser(description="""Takes pairwise vcf files and outputs into a combined table.""")
parser.add_argument('file',type=argparse.FileType('r'), nargs='+',help="""Input pairwise files for reading.""")
parser.add_argument('gene',type=argparse.FileType('r'),help="""This is a gff file.""")
parser.add_argument('-b','--bed',help="""If using an 8 column bed file, specify with this
argument.""",action='store_true')
parser.add_argument('-v','--verbose',help="""Displays verbose output.""",action='store_true')
args = parser.parse_args()

timein = time.time()
# f is the combined file
files = list()
for csv in range(0, len(args.file)):
	files.append(pd.read_csv(args.file[csv], delimiter='\t', index_col=0))
	if csv == 0:
		f = files[0]
	else:
		f = pd.concat([f, files[csv]], axis=1)

names = f.columns.values[:]

out = args.gene.name.split('/')[-1][0:-4] + '_' + '_'.join(map(str,names)) + '.tbl'
# f.to_csv(path_or_buf=out, sep='\t', na_rep='.')

# read in the pairwise differenced files
# create a table with that data
# output both the [gnee : SNP : indicator] file and the [gene : indicators : count] file

# Read in output of the previous script

# POS is column 1 (zero-based)
# Identify if ref or sample has SNP
# record 1 for has SNP and 0 for no SNP

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
			f.set_value(f.index[pos], "Gene", g.index[gene])
			gene -= 1 # deal with the next SNP being in the same gene
			break
		elif gene == len(g.index) - 1:
			if args.verbose:
				print('SNP\t' + str(pos) + '\tat position:\t'  + str(f.index[pos]) + '\tis not in any gene.')
			gene = g_count - 1 # since has run through the entire list, reset to previous found gene
			f.set_value(f.index[pos], "Gene", '.')
			break

g.loc[:, 'Count'] = g[range(2, len(g.columns))].astype(bool).sum(axis=1)
# print out the other file
f = pd.concat([f, f.sum(axis=1, skipna=True)], axis=1)
f.columns.values[-1] = 'Sum'

# rearrange the columns
cols = f.columns.tolist()
cols = [cols[-2]] + cols[:-2] + [cols[-1]]
f = f[cols]
f.to_csv(path_or_buf=out, sep='\t', na_rep='.')

out = out[0:-4] + '.comb'
g.drop(['start', 'stop'], axis=1, inplace=True)
g = g[(g.T != 0).any()]
g.to_csv(path_or_buf=out, sep='\t')

if args.verbose:
	print('Elapse: ' + str(time.time()-timein))


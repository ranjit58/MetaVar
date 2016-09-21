#/bin/python

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

parser = argparse.ArgumentParser(description="""Takes pairwise vcf files and outputs into a combined table.""")
parser.add_argument('file',type=argparse.FileType('r'), nargs='+',help="""Input pairwise files for reading.""")
args = parser.parse_args()

files = list()
for csv in range(0, len(args.file)):
	files.append(pd.read_csv(args.file[csv], delimiter='\t', index_col=0))
	if csv == 0:
		combined = files[0]
	else:
		combined = pd.concat([combined, files[csv]], axis=1)

names = combined.columns.values[:]
combined = pd.concat([combined, combined.sum(axis=1, skipna=True)], axis=1)
combined.columns.values[-1] = 'Sum'
pdb.set_trace()
out = '_'.join(map(str,names)) + '.txt.tbl'
combined.to_csv(path_or_buf=out, sep='\t', na_rep='.')
pdb.set_trace()


from time import clock
import argparse
import pdb
from csv import reader

start = clock()
pipeline_flag = 0

if True:
	parser = argparse.ArgumentParser(description="""Provide samples and run the MetaVar analysis pipeline.""")
	parser.add_argument('vcf',help="""Specify the vcf file.""")
	parser.add_argument('pair',help="""Specify a file with sample pairings.""")
	parser.add_argument('-i', '--intermediate', help="Specify to save intermediate files", action='store_true')
	parser.add_argument('gene',help="""Specify a file with gene information.""")
	parser.add_argument('-t','--type', help="""Specify if gene file is a .bed file.""", action='store_true')
	args = parser.parse_args()

inter = args.intermediate # intermediate files, default 0
vcf = args.vcf
gene = args.gene
g_file_type = args.type

# if args exists, then pipe_line_flag is True
try:
	args
	pipeline_flag = 1
except NameError:
	pass

# read in all the pairs into a list
with open(args.pair) as p:
	pairs = list(reader(p, delimiter="\t"))
# loop over each pair
  # get_pairwise and save each pair file (optionally)
  # extract each pair and save file (optionally)

all_data = list() # store all the extracted pairwise data

snp_count = []
g_count = []

for pair in pairs:
	if pairs.index(pair) > 0:
		reload(get_paired_vcf2)
		from get_paired_vcf2 import data, names
	else:
		import get_paired_vcf2
		from get_paired_vcf2 import data, names

	snp_count.append(names[:])
	all_data.append(data)
snp_count = ''.join(['_'.join([str(x[0]) + '_' + str(x[1]) for x in snp_count]), '.txt'])
g_count = snp_count + '.comb'


extracted_time = clock()
print('Start : Extracted, elapse: ' + str(extracted_time - start) + ' sec.\n')

# aggregate all this data
import aggregate_genomic_diff2
from aggregate_genomic_diff2 import pos_tbl, gene_dict
aggregated_time = clock()
print('Extract : Aggregate, elapse: ' + str(aggregated_time - extracted_time) + ' sec.\n')
pdb.set_trace()






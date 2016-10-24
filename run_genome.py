from time import clock
import argparse
import pdb
from csv import reader

start = clock()
pipeline_flag = 0

if True:
	parser = argparse.ArgumentParser(description="""Provide samples and run the MetaVar analysis pipeline.""")
	parser.add_argument('-v', '--vcf',help="""Specify the multi-sample vcf file.""")
	parser.add_argument('-p', '--pair',help="""Specify a file with sample pairings (the samples in the multi-sample vcf).""")
	parser.add_argument('-i', '--intermediate', help="Specify to save intermediate files", action='store_true')
	parser.add_argument('-g', '--gene',help="""Specify a file with gene information (by default .gff or with -t an 8 column .bed).""")
	parser.add_argument('-t','--type', help="""Specify if gene file is a .bed file.""", action='store_true')
	parser.add_argument('-o','--output',help="""Specify the name of an output directory.""")
	args = parser.parse_args()

inter = args.intermediate # intermediate files, default 0
vcf = args.vcf
if args.output is not None:
	if args.output[-1] == '/':
		args.output = args.output[-1] = []
	final_name = args.output + '/' + vcf.split('/')[-1].split('.')[0]
else:
	final_name = vcf.split('/')[-1].split('.')[0]
gene = args.gene
g_file_type = args.type
final = 1 # print out final files

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
	# run the get_paired script for each file
	if pairs.index(pair) > 0:
		# for all items except the first
		reload(get_paired_vcf)
		from get_paired_vcf import data, names
	else:
		# run it for the first time
		import get_paired_vcf
		from get_paired_vcf import data, names

	snp_count.append(names[:])
	all_data.append(data)

extracted_time = clock()
#print('Start : Extracted, elapse: ' + str(extracted_time - start) + ' sec.\n')

# aggregate all this data
import aggregate_genomic_diff
from aggregate_genomic_diff import pos_tbl, gene_dict
aggregated_time = clock()
#print('Extract : Aggregate, elapse: ' + str(aggregated_time - extracted_time) + ' sec.\n')






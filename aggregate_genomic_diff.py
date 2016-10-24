from csv import reader
import numbers
import pdb
try:
	from __main__ import pipeline_flag, final, all_data, gene, g_file_type, g_count, snp_count, final_name
except ImportError:
	# if running as a script
	pipeline_flag = 0

def print_to_file(tbl, path):
	for row in tbl:
		path.write('\t'.join([str(col) for col in row]) + '\n')

def get_directionality(flag, row):
	if flag: # 0:1
		pos = [x for x in range(0, len(row)) if x % 2 == 0]
	else: # 1:0
		pos = [x for x in range(0, len(row)) if x % 2 == 1]
	return sum([row[p] for p in pos if isinstance(row[p], numbers.Number)])

if not pipeline_flag:
	final = 1
	parser = argparse.ArgumentParser(description="""Take pairwise vcf files and outputs into a combined table.""")
	parser.add_argument('file',type=argparse.FileType('r'), nargs='+',help="""Input pairwise files for reading.""") 
	parser.add_argument('gene',type=argparse.FileType('r'),help="""This is a gff file.""")
	parser.add_argument('-b','--bed',help="""If using an 8 column bed file, specify with this argument.""",action='store_true')
	parser.add_argument('-v','--verbose',help="""Displays verbose output.""",action='store_true') 
else:
	# get column names
	names = list()
	for x in snp_count:
		names.append(x[0])
		names.append(x[1])
	names.insert(0, 'gene')
	names.insert(0, 'snp')
	names.append('sum')
	names.append('dir01')
	names.append('dir10')
	names.append('per')
	snp_count = final_name + '_coord.txt'
	g_count = final_name + '_gene.txt'
	#snp_count = ''.join(['_'.join([str(x[0]) + '_' + str(x[1]) for x in snp_count]), '.txt'])
	#g_count = snp_count + '.comb'


# read in gene file
with open(gene) as g:
	genes = list(reader(g, delimiter='\t'))
if g_file_type:
	pass
else:
	start = 3
	end = 4
	gtype = 8
	glength = 9
	row_ident = 2

# get the gene name, gene start position, gene end position
genes = [[gene[gtype].split(';')[0].split('=')[1], int(gene[start]), int(gene[end])] for gene in genes if len(gene) == glength and gene[row_ident] == 'CDS']
# identify unique snps, store in table, check if each extracted file in all_data has the snp, if yes increment in row
unique_snps = set() # as rows, then push the 1 or 0 for each file in the extracted data (in a specified order)
for col in all_data:
	unique_snps.update([sub[0] for sub in col]) # get the unique snps for each

# match each snp to a gene
snps_to_genes = [[snp, gene[0]] for snp in unique_snps for gene in genes if gene[1] <= snp and gene[2] >= snp]
snps_to_genes.sort()

pos_tbl = []
flag = 0

# identify the snp:gene counts for extracted data
for pos in snps_to_genes: # go by row
	row = [pos[0], pos[1]]
	for col in all_data: # by column
		for sub in col: # add element to list
			if sub[0] == pos[0]:
				row.append(sub[1])
				row.append(sub[2])
				flag = 1 # stop searching for the snp
				break # continue to next col (next extracted pairwise vcf)
		if flag != 1: # no snp was found, so report no snp
			row.append('.')
			row.append('.')
		else:
			flag = 0
	
	row.append(sum([x for x in row[2:] if isinstance(x, numbers.Number)])) # get the count
	# get the directionality count : 0 1
	row.append(get_directionality(0, row[2:-1]))
	# get the direcitonality count : 1 0
	row.append(get_directionality(1, row[2:-2]))
	# get the percentage : 0 1
	row.append(row[-2] / (row[-1] + float(row[-2])) * 100)
	pos_tbl.append(row)

if final:
	# print to file
	with open(snp_count, 'w+') as s:
		s.write('\t'.join([col for col in names]) + '\n')
		print_to_file(pos_tbl, s)

names.remove('snp') # set names to be acceptable for the gene_dict
names.remove('sum')
names.append('count')
names.append('sum')

snps_per_gene = {snp: gene for (snp, gene) in snps_to_genes} # get dict of snp keys with gene values
gene_dict = {gene: [] for (snp, gene) in snps_to_genes}
# identify the number of snps per gene for extracted data
for col in all_data:
	temp_gene_dict = {gene: [0, 0] for (snp, gene) in snps_to_genes}
	for snp in col:
		try:
			gene = snps_per_gene[snp[0]]
			temp_gene_dict[gene] = [temp_gene_dict[gene][0] + snp[1], temp_gene_dict[gene][1] + snp[2]]
		except KeyError:
			continue # for snps not located in genes
	# add temp to real
	for gene in gene_dict:
		gene_dict[gene].append(temp_gene_dict[gene])

# get count for all the genes
for gene in gene_dict:
	gene_dict[gene] = reduce(lambda x,y: x + y, gene_dict[gene])
	gene_dict[gene].append(sum(x > 0 for x in gene_dict[gene])) # count
	gene_dict[gene].append(sum(x for x in gene_dict[gene][0:-2])) # sum, not counting the count column
if final:
	# print to file
	with open(g_count, 'w+') as g:
		g.write('\t'.join([col for col in names]) + '\n')
		for gene in gene_dict:
			g.write(gene + '\t' + '\t'.join(str(x) for x in gene_dict[gene]) + '\n')



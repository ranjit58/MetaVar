from csv import reader
import numbers
import pdb
from __main__ import pipeline_flag, inter, all_data, gene, g_file_type, g_count, snp_count

# read in gene file
with open(gene) as g:
	genes = list(reader(g, delimiter='\t'))
if g_file_type:
	pass
else:
	start = 3
	end = 4
	gtype = 2
	glength = 9

# get the gene name, gene start position, gene end position
genes = [[gene[gtype], int(gene[start]), int(gene[end])] for gene in genes if len(gene) is glength and gene[gtype][0:4] == 'gene']

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
	pos_tbl.append(row)

if inter:
	# print to file
	with open(snp_count, 'w+') as s:
		pass

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
	gene_dict[gene].append(sum(x > 0 for x in gene_dict[gene]))

if inter:
	# print to file
	with open(g_count, 'w+') as g:
		pass




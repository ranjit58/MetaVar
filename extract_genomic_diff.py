# Input: the output of the get_paired_vcf.py file and a gff file
# TO-DO: identify the differences and map to a gene

# read in the gff file to find in which gene the location of the SNP difference was
# Record the gene and the location in the gene and the file with the SNP
# Save this to a file with the species name, then allow the other t2 files to append their data to the table

# Example file:

## Bacteroides_vulgatus
# t1	t2	gene	location (bp)
# 1	0	3	46500
# 0	1	18	180049

# t1	t3	gene	location (bp)
# 1	0	1	2500
# 0	1	3	4800

# separate files for different t1 files

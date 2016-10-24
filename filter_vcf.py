import pdb
from glob import glob
from sys import exit
from csv import reader, writer

def print_to_file(out, csv):
	for row in csv:
		out.write('\t'.join(row) + '\n')

paths = ['/data/scratch/rkumar/work/METAG-COMMON/SNP-FILTER/*.exonic*'
,'/data/scratch/rkumar/work/METAG-PROJ/JG-BIG/GATK-MULTISNP/*/*.vcf', '/data/scratch/bdesilva/MetaVar/filtered_vcfs/']

# read in the folders with the data
ff = glob(paths[0])
ff.sort()
vcfs = glob(paths[1])
vcfs.sort()

out_vcf = [paths[2] + vcf.split('/')[-1] for vcf in vcfs]

# check to see that each folder has the same number of specific files
if len(ff) != len(vcfs):
	exit('Number of files in filter_file_folder is not equal to the number of files in the vcf files folder.')

# for each file
for i in range(0, len(ff)):
	with open(ff[i]) as fil, open(vcfs[i]) as vcf, open(out_vcf[i], 'w') as out:
		# filter the filter file for not 'synonymous' or 'unknown'
		f_csv = list(reader(fil, delimiter='\t'))
		f_csv = [int(row[4]) for row in f_csv if row[1] != 'synonymous SNV' and row[1] != 'unknown']
		f_csv.sort()
		
		# filter the vcf
		v_csv = list(reader(vcf, delimiter='\t'))
		v_csv = [row for row in v_csv if row[0][0] == '#' or int(row[1]) in f_csv]
		print_to_file(out, v_csv)

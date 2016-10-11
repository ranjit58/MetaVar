# MetaVar - Exploring genomic variation in metagenomic datasets

## Workflow
run_genome.py is the pipeline main script
* will need to change the reload command for python 3, so run on python 2

Example workflow:
python run_genome.py example/Bacteroides_vulgatus.vcf.snp.gatk pair_file.txt example/Bacteroides_vulgatus.gff
* can specify -i for intermediate files
* default output is the two files with snp count per gene and snps per file

## Workflow Description
1. extract pairwise vcf files
* extract the SNP differences
* merge individual .diff files into a table
* using a gff or bed file, lookup in what genes the SNP differences are occuring and output to a combined file

* output a file for GeneBrowser viewing
* do analysis


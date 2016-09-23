# MetaVar - Exploring genomic variation in metagenomic datasets

## Workflow
##### Will have to move some files around at this point
* python get_paired_vcf.py example/Bacteroides_vulgatus.vcf.snp.gatk D11 R11
* python get_paired_vcf.py example/Bacteroides_vulgatus.vcf.snp.gatk D8 R8
* python get_paired_vcf.py example/Bacteroides_vulgatus.vcf.snp.gatk D16 R16

* python extract_genomic_diff.py D11_R11.txt
* python extract_genomic_diff.py D8_R8.txt
* python extract_genomic_diff.py D16_R16.txt

* python merge_genes.py example/D8_R8.txt.diff example/D11_R11.txt.diff example/D16_R16.txt.diff 

* python aggregate_genomic_diff.py example/D8_R8_D11_R11_D16_R16.txt.tbl example/Bacteroides_vulgatus.gff


## Workflow Description
1. extract pairwise vcf files
* extract the SNP differences
* merge individual .diff files into a table
* using a gff or bed file, lookup in what genes the SNP differences are occuring and output to a combined file

* output a file for GeneBrowser viewing
* do analysis


# MetaVar - Exploring genomic variation in metagenomic datasets

## Workflow

python get_paired_vcf.py example/Bacteroides_vulgatus.vcf.snp.gatk D11 R11

python extract_genomic_diff.py D11_R11.txt

python aggregate_genomic_diff.py example/D11_R11.txt.diff example/Bacteroides_vulgatus.bed -v


## Workflow 1
* extract pairwise vcf files
* extract the SNP differences
* using a gff or bed file, lookup in what genes the SNP differences are occuring
* output a file for GeneBrowser viewing
* output data about the gene changes (only the changed genes)
* do analysis
  * % change of the gene, % change of each gene out of total changes, number of changes in each gene
  * some analysis on where the changes occured (?)


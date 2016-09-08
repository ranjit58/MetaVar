# MetaVar - Exploring genomic variation in metagenomic datasets

## Workflow 1
* extract pairwise vcf files
* using a gff file, lookup in what genes the SNP differences are occuring
* output a file for GeneBrowser viewing
* output data about the gene changes (only the changed genes)
  * % change of the gene, % change of each gene out of total changes, number of changes in each gene
  * some analysis on where the changes occured (?)

## Workflow 2 - 1 script with functions
* Could probably do this all in one script
* just read in specifically
  * the multisample vcf
  * [t1 name/position, t2 name(s)/position(s)]
  * the gff file
  or 
  * a configuration file with the specified t1:t2:gff triplets (even for the entire species)
    * config example:

> #### Bacteroides_vulgatus
> Bacteroides_vulgatus.gff
>
> T1 file | T2 file
> --- | ---
> T1.vcf | T2.vcf
> T1.vcf | T3.vcf
> T12.vcf | T22.vcf
> T12.vcf | T32.vcf
> 
> #### Bacteroides_ovatus
> Bacteroides_ovatus.gff
> 
> T1 file | T2 file
> --- | ---
> T1.vcf | T2.vcf
> T1.vcf | T3.vcf
> T12.vcf | T22.vcf
> T12.vcf | T32.vcf


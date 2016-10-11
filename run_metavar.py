#! /bin/python

import os
import sys

# parser and subparser
# specify the point at which the pipeline is being entered
# specify the necessary parameters for the pipeline point
	
	# 0 (or none as default)
	# read in either a folder of genome files or read in + number of genome files
	# read in multi-sample vcf file

	# 1 (skip get_paired_vcf)
	# read in either a folder of genome files or read in + number of genome files
	# read in either a folder with the pairwise file names or + number of parameters
	  # parameters will be donor recipient separated, if uneven number, then the last one is cut off
	
	# 2 (skip extract_genomic_diff)
	# read in either a folder of genome files or read in + number of genome files
	# read in either a folder with the extracted files or + number of parameters 
	  # parameters will be donor recipient separated, if uneven number, then the last one is cut off




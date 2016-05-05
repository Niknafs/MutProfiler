#! /bin/bash

# MutProfiler: 
# a brief collection of wrappers to generate 
# allelic depth tables for single nucleotide variants
# from a bam file.
#
# Usage:
# bash profile.sh muts.vcf sample.bam hg19.fa muts
#
# muts.vcf: input vcf file with mutated positions
# sample.bam: bam file from which the allelic counts will be calculated
# hg19.fa: reference sequence
# muts: output prefix
#

# Requirements:
# 1) samtools is present on system path
#    to check this, call 'which samtools' from the 
#    commandline. It should return the path from 
#    which you are running samtools
# 

src="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

inputVcf=$1
inputBam=$2
refSequence=$3
outputPrefix=$4

# (1)
# generate a set of SNPs from the vcf file
python $src/extract-snps.py \
    -i $inputVcf \
    -o $outputPrefix

# (2)
# generate mpileup for SNP positions
date
echo "Generating mpileup at SNP positions from $inputBam"
rm $outputPrefix.SNP.mpileup
bash $src/mpileup.sh \
    $outputPrefix.SNP.ranges \
    $refSequence \
    $inputBam \
    $outputPrefix.SNP

# (3) generate allelic table for SNP positions
date
echo "Generating mutation allelic table from mpileup"
python $src/make-allelic-table.py \
    -s $outputPrefix.SNP.table \
    -m $outputPrefix.SNP.mpileup \
    -o $outputPrefix.allelic.table

nOriginal=$(wc -l $outputPrefix.SNP.table | cut -d ' ' -f1)
nFinal=$(wc -l $outputPrefix.allelic.table | cut -d ' ' -f1)
nFinal=$(echo "$nFinal - 1" | bc)
echo "SNP allelic table available at $outputPrefix.allelic.table containing ${nFinal}/${nOriginal} of initial SNPs."
date

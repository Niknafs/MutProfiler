# MutProfiler

MutProfiler is a  collection of wrappers to generate  allelic depth tables for single nucleotide variants from a bam file.

# Usage
```
bash profile.sh muts.vcf sample.bam hg19.fa muts
```

* `muts.vcf`: input vcf file with mutated positions
* `sample.bam`: bam file from which the allelic counts will be calculated
* `hg19.fa`: reference sequence
* `muts`: output prefix

# Requirements

Assumes `samtools` is present on system path. To check this, call
```
which samtools
```
from the commandline. It should return the path from which you are running samtools.


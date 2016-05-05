#! /usr/bin/env python
import sys
import os
import collections

from argparse import ArgumentParser as argument_parser

sys.path.append(os.path.realpath(__file__))
from baseParser import parseString

class InputParser(object):
    def __init__(self):
        parser = argument_parser()
        parser.add_argument('-m','--mpileup', help = 'mpileup path')
        parser.add_argument('-s','--snps', help = 'snp table path')
        parser.add_argument('-o','--output', help = 'output path')
        args = parser.parse_args()
        self.__dict__.update(args.__dict__)

def read_snp_table(path):
    snps = {}
    for line in file(path):
        toks = line.strip().split('\t')
        chrom, pos, strand, ref, alt = toks
        snps[(chrom, pos)] = [strand, ref, alt]
    return snps

def read_mpileup(path):
    pileups = {}
    f_h = file(path)
    for line in f_h:
        toks = line.strip().split('\t')
        chrom, pos, ref, cov, alleleString , quals = toks
        pileups[(chrom,pos)] = [ref, cov, parseString(ref, alleleString)]
    f_h.close()
    return pileups

def write_allelic_table(snps, pileups, path):
    f_w = file(path, 'w')
    print >>f_w, '\t'.join(['chrom','pos','ref','alt', 'cov' , \
                            'variant.allele.freq',
                            'ref.count','alt.count',\
                            'forward.ref','reverse.ref',\
                            'forward.alt','reverse.alt'])
    
    nFail = 0
    for chrom, pos in snps.keys():
        strand, ref, alt = snps[(chrom, pos)]
        
        if (chrom, pos) not in pileups.keys():
            # for some reason, no pileup line was generated for this input
            nFail += 1
            print >>sys.stderr, 'No pileup available for %s:%s:%s,%s'%(\
                                        chrom, pos, ref, alt)
            continue
        
        Ref, cov, counts = pileups[(chrom, pos)]
        counts = counts.types
        refForward = counts[ref.upper()]
        refReverse = counts[ref.lower()]
        altForward = counts[alt.upper()]
        altReverse = counts[alt.lower()]
        
        refCount = refForward + refReverse
        altCount = altForward + altReverse
        
        if float(cov) == 0:
            vaf = 'NA'
        else:
            vaf = '%0.4f'%(float(altCount) / float(cov))

        print >>f_w, '\t'.join(map(str, [chrom, pos, ref, alt, cov, \
                                vaf, refCount, altCount,\
                                refForward, refReverse,\
                                altForward, altReverse]))
    f_w.close()
    
    if nFail != 0:
        print >>sys.stdout, 'Skipped %d SNP positions due to lack of mpileup'%nFail

def main():
    args = InputParser()
    
    snps = read_snp_table(args.snps)
    pileups = read_mpileup(args.mpileup)
    write_allelic_table(snps, pileups, args.output)
    

if __name__ == '__main__':
    main()

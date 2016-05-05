#! /usr/bin/env python
import sys
import os
import collections

from argparse import ArgumentParser as argument_parser

nucs = ['A','C','G','T']

class InputParser(object):
    def __init__(self):
        parser = argument_parser()
        parser.add_argument('-i','--input', help = 'input path')
        parser.add_argument('-o','--output', help = 'output path')
        args = parser.parse_args()
        self.__dict__.update(args.__dict__)

def extract_snps(inputPath, outputPath):
    # a VCF input
    f_h = file(inputPath)
    f_s = file(outputPath + '.SNP.table', 'w')
    f_i = file(outputPath +  '.Indel.table','w')
    f_r = file(outputPath +  '.SNP.ranges', 'w')
    
    line = f_h.readline()
    nSNP = 0
    nIndel = 0

    while line.startswith('#'):
        line = f_h.readline()

    while True:
        toks = line.strip().split('\t')
        if toks == ['']: break
        chrom, pos, tag, ref, alt = toks[:5]

        if ref in nucs and alt in nucs:
            print >>f_s, '\t'.join([chrom, pos, '+', ref, alt])
            print >>f_r, chrom + ':' + pos + '-' + pos
            nSNP += 1
        elif ',' in alt:
            alts = alt.split(',')
            for alt in alts:
                print >>f_s, '\t'.join([chrom, pos, '+', ref, alt])
                print >>f_r, chrom + ':' + pos + '-' + pos
            nSNP += 1
        else:
            print >>f_i, '\t'.join([chrom, pos, '+', ref, alt])
            nIndel += 1
        
        line = f_h.readline()
        

    f_h.close()
    f_s.close()
    f_r.close()
    f_i.close()

    print >>sys.stdout, '%d SNPs and %d Indels present in input VCF.'%(nSNP, nIndel)
    print >>sys.stdout, 'Proceeding to generate allelic depth table for %d SNPs.'%(nSNP)
    

def main():
    args = InputParser()
    extract_snps(args.input, args.output)

if __name__ == '__main__':
    main()

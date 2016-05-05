#! /usr/bin/env python
# most recently copied over from /projects/clonal-evolution/Mouse/C2/exprs/baf/scripts/
###############################################################################
# copied over from /projects/clonal-evolution/Human/results/ASCAT/scripts/
###############################################################################
# parses pileup base string and returns the counts for all possible alleles 
# for each position
# reads input (mpileup output) from sys.stdin
# copied over from /projects/clonal-evolution/Human/results/mutect/Pam03/drilldown/scripts
###############################################################################

import os
import sys

class parseString(object):
    
    def __init__(self, ref, string):
        self.string = string
        self.ref = ref
        self.types = {'A':0,'C':0,'G':0,'T':0, \
                      'a':0,'c':0,'g':0,'t':0, \
                      '-':[],'*':0,'+':[],'X':[]}
        self.process()
        
    def process(self):
        # remove end of read character
        self.string = self.string.replace('$','')
        while self.string != '':
            if self.string[0] == '^':
                # skip two characters when encountering '^' as it indicates
                # a read start mark and the read mapping quality
                self.string = self.string[2:]
            elif self.string[0] == '*':
                self.types['*'] += 1
                # skip to next character
                self.string = self.string[1:]
            
            elif self.string[0] in ['.',',']:
                if (len(self.string)== 1) or (self.string[1] not in ['+','-']):
                    # a reference base
                    if self.string[0] == '.':
                        self.types[self.ref.upper()] += 1
                    elif self.string[0] == ',':
                        self.types[self.ref.lower()] += 1
                    self.string = self.string[1:]
    
                elif self.string[1] in ['+','-']: 
                    enum = ""
                    i = 2
                    while self.string[i] in map(str, range(10)):
                        enum += self.string[i]
                        i += 1
                    
                    indelLength = int(enum)
                    indelSeq = self.string[:2] + self.string[i:i+indelLength]
                    self.types[self.string[1]].append(indelSeq)
                    self.string = self.string[i+indelLength:]
                    
            elif self.types.has_key(self.string[0]) and\
                 ((len(self.string)==1) or (self.string[1] not in ['-','+'])):
                # one of the four bases
                self.types[self.string[0]] += 1
                self.string = self.string[1:]
            elif (self.types.has_key(self.string[0])) and (self.string[1] in ['-','+']):
                enum = ""
                i = 2
                while self.string[i] in map(str, range(10)):
                    enum += self.string[i]
                    i += 1
                indelLength = int(enum)
                indelSeq = self.string[:2] + self.string[i:i+indelLength]
                self.types[self.string[1]].append(indelSeq)
                self.string = self.string[i+indelLength:]

            else:
                # unrecognized character
                # or a read that reports a substitition followed by an insertion/deletion
                self.types['X'].append(self.string[0])
                self.string = self.string[1:]
        return
    def __repr__(self):
        types = self.types
        return '\t'.join(map(str,[types['A'], types['a'], types['C'],types['c'],\
                                  types['G'], types['g'], types['T'],types['t'], \
                                  types['*']]) +\
                         map('/'.join, [types['-'],types['+'],types['X']]))
        

def main():
    print >>sys.stdout, "chrom\tpos\tref\tcov\tA\ta\tC\tc\tG\tg\tT\tt\t*\t-\t+\tX"
    for line in sys.stdin:
        toks = line.strip('\n').split('\t')
        ref = toks[2].upper()
        cov = toks[3]
        print >>sys.stdout, '\t'.join([toks[0], toks[1],ref, cov]) + '\t' + \
            parseString(ref, toks[4]).__repr__()

if __name__ == '__main__':
    main()

#! /usr/bine/env python

import os,sys
import re

'''
A small wrapper script to run hmmtop and return relevant information
'''

def run_hmmtop(infile,outfile):

    os.system('hmmtop -if={} -of={} 2> /dev/null'.format(infile,outfile))

    no_tms = 0

    with open(outfile,'r+') as f:

        for line in f:

            groups = re.match('\>.+\s+(IN|OUT)\s+(\d+)\s+(.+)\n',line)

            if groups != None:

                no_tms = groups.group(2)

    return no_tms


if __name__ == "__main__":

    infile = sys.argv[1]

    outfile = sys.argv[2]

    run_hmmtop(infile,outfile)

#! /usr/bin/env python3

import argparse
import os,sys
import subprocess as sp
from Bio import AlignIO
from run_hmmtop import run_hmmtop

"""
A tool developed to standardize the alignment statistics used for comparative proteomic analysis
in the Saier Lab at UCSD. Currently, protein sequences are acquired from BLAST databases using
blastdbcmd and all alignments are performed using ssearch36.
"""

def setup(outdir):
    """
    Handles Creation of Output Directory Structure

    Parameters
    ----------
    outdir
        the user provided path to an output directory

    Returns
    -------
    seqDir
        the path to the directory where sequence files will be stored for alignment
    alnDir
        the path to the directory where alignment files will be stored
    hmmDir
        the path to the directory where the output of hmmtop output will be stored
    """
    #check for directory. Create if not present.
    if not os.path.isdir(outdir):

        os.makedirs(outdir)

    #make a seqs folder for sequences
    seqDir = '{}/seqs'.format(outdir)

    if not os.path.isdir(seqDir):
        os.makedirs(seqDir)

    #make an alignment folder for alignment files
    alnDir = '{}/aln'.format(outdir)

    if not os.path.isdir(alnDir):
        os.makedirs(alnDir)

    #make a directory for hmmtop output
    hmmDir = '{}/hmmtop'.format(outdir)

    if not os.path.isdir(hmmDir):
        os.makedirs(hmmDir)

    return seqDir,alnDir,hmmDir


def alignSeq(infile, outdir, outfile, seqDir, alnDir, hmmDir, tcdb_db, query_db):
    """
    Collects sequences for relevant proteins from input file and performs alignments and
    TransMembrane Sequence (TMS) prediction

    Parameters
    ----------
    infile
        the path to the input file
    outdir
        the path to the output directory
    outfile
        the name of the tsv containing the alignment statistics (not including file extension)
    seqDir
        the path to the directory where the sequence will be stored
    alnDir
        the path to the directory where alignment files will be stored
    hmmDir
        the path to the directory where the hmmtop output will be stored
    """
    #read infile
    contents = open(infile,'r').readlines()

    #create outfile
    out = open('{}/{}.tsv'.format(outdir,outfile),'w')
    out.write('#query\tq_tms\tacc\ts_tms\ttcid\tevalue\tpident\tqcov\tscov\n')

    tms = {}

    for line in contents:

        if line[0][0] == '#':
            continue

        query,acc,tcid = line.rstrip().split('\t')

        #check if version number in query
        if '.' in query:
            query = query.split('.')[0]

        #check for query protein sequence
        querySeq = '{}/{}.faa'.format(seqDir,query)

        if not os.path.exists(querySeq):
            os.system('blastdbcmd -db {} -entry {} -target_only > {}'.format(query_db,query,querySeq))
            tms[query] = run_hmmtop(querySeq,'{}/{}.out'.format(hmmDir,query))

        #check if version number in accesion
        if '.' in acc:
            acc = acc.split('.')[0]

        #check for tcdb protein
        tcSeq = '{}/{}.faa'.format(seqDir,acc)

        if not os.path.exists(tcSeq):
            os.system('blastdbcmd -db {} -entry {}-{} -target_only > {}'.format(tcdb_db,tcid,acc,tcSeq))
            tms[acc] = run_hmmtop(tcSeq,'{}/{}.out'.format(hmmDir,acc))

        #perform alignments
        aln = '{}/ssearch36_{}_vs_{}.aln'.format(alnDir,query,acc)

        if not os.path.exists(aln):
            os.system('ssearch36 -z 11 -k 1000 -s BL50 -E 1 -W 0 -m 10  {} {} > {}'.format(querySeq,tcSeq,aln))

        alignments = AlignIO.parse(open(aln),'fasta-m10')

        for alignment in alignments:

            evalue = alignment._annotations['sw_expect']
            pident = float(alignment._annotations['sw_ident'])*100
            qcov,scov = [(int(x._al_stop)-int(x._al_start))/float(len(x.seq))for x in alignment]

            out.write('{}\n'.format('\t'.join(map(str,[query,tms[query],acc,tms[acc],tcid,evalue,pident,qcov,scov]))))

    out.close()


def parse_arguments()
    """
    Argument Parser for the CLI
    """

    desc =''' A tool developed to standardize the alignment statistics used for comparative proteomic analysis
    in the Saier Lab at UCSD. Currently, protein sequences are acquired from BLAST databases using
    blastdbcmd and all alignments are performed using ssearch36.'''

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-i', '--infile', action='store',
                        help='The path to the tsv file containing the results of a proteome analysis')
    parser.add_argument('-of', '--outfile', action='store', default='results',
                        help='The name for the file containing alignment statistics (without the file extension), ' \
                        'which will be place in the output directory. Default is results')
    parser.add_argument('-od', '--outdir', action='store', default='./output',
                        help='The path to the directory where all the analysis files will be output. Default is ./output')
    parser.add_argument('-tc', '--tcdb_db', action='store', default='tcdb',
                        help='The path to the tcdb blastdb. By default, the value is tcdb')
    parser.add_argument('-q', '--query_db', action='store', default='nr',
                        help='The path to the blastdb for the query proteome. By default, the value is nr')

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    infile = args.infile
    if infile is None:
        print("Input TSV Required to Run Alignment!")
        parser.print_help()
        sys.exit(0)

    return args.infile, args.outdir, args.outfile, args.tcdb_db, args.query_db

if __name__ == "__main__":
    """
    Main function of the program
    """
    infile, outdir, outfile, tcdb_db, query_db = parse_arguments()

    seqDir, alnDir, hmmDir = setup(outdir)

    alignSeq(infile, outdir, outfile, seqDir, alnDir, hmmDir, tcdb_db, query_db)

#! /usr/bin/env python

import os,sys
import subprocess as sp
from Bio import AlignIO

'''
ssearch36 -z 11 -k 1000 -s $subMatrix -E $evalue -W 0 -m 0  $qfile $sfile > $alnFile
'''

def setup(outdir):

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

    
    return seqDir,alnDir

def alignSeq(infile,outdir,outfile,seqDir,alnDir):

    #read infile 
    contents = open(infile,'r').readlines()[1:]

    #create outfile
    out = open('{}/{}.tsv'.format(outdir,outfile),'w') 
    out.write('#query\tacc\ttcid\tevalue\tpident\tqcov\tscov\n')


    for line in contents:

        query,acc,tcid = line.rstrip().split('\t')


        #check if version number in query

        if '.' in query:

            query = query.split('.')[0]

        #check for query protein sequence
        querySeq = '{}/{}.faa'.format(seqDir,query)

        if not os.path.exists(querySeq):

            os.system('blastdbcmd -db nr -entry {} -target_only > {}'.format(query,querySeq))

        #check if version number in accesion
        if '.' in acc:

            acc = acc.split('.')[0]

        #check for tcdb protein
        tcSeq = '{}/{}.faa'.format(seqDir,acc)

        if not os.path.exists(tcSeq):

            os.system('blastdbcmd -db tcdb -entry {}-{} -target_only > {}'.format(tcid,acc,tcSeq))


        #perform alignments
        aln = '{}/ssearch36_{}_vs_{}.aln'.format(alnDir,query,acc)

        if not os.path.exists(aln):

            os.system('ssearch36 -z 11 -k 1000 -s BL50 -E 1 -W 0 -m 10  {} {} > {}'.format(querySeq,tcSeq,aln))


        #try:
        
            #print(aln)

        alignments = AlignIO.parse(open(aln),'fasta-m10')

            #print(vars(alignment))

        for alignment in alignments:

            evalue = alignment._annotations['sw_expect']
            pident = float(alignment._annotations['sw_ident'])*100
            
            qcov,scov = [(int(x._al_stop)-int(x._al_start))/float(len(x.seq))for x in alignment]

            out.write('{}\n'.format('\t'.join(map(str,[query,acc,tcid,evalue,pident,qcov,scov]))))
           
        '''
        for record in alignment:

        print(record.seq)
        print(record._al_start,record._al_stop)
                
        print('\n\n')
        '''
        #except Exception as e:

            #print(e)
            #print(alignment)


if __name__ == "__main__":

    infile = sys.argv[1]
    outdir = sys.argv[2]
    outfile = sys.argv[3]

    seqDir,alnDir = setup(outdir)

    alignSeq(infile,outdir,outfile,seqDir,alnDir)

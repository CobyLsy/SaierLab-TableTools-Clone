# Table-Tools
A collection of scripts developed to support ongoing comparative proteomics research in the Saier Lab at the University of California, San Diego.

## Requirements
Currently, there are some programs that need to be installed on the system in order to be able to execute one of the main script, evaluateAlignments.py. These are:

* [blastdb](https://www.ncbi.nlm.nih.gov/books/NBK279690/ "BLAST Manual")

   We utilize local BLAST databases to store and access sequences from TCDB and any metagenomes used in our research.

* [_ssearch36_](https://fasta.bioch.virginia.edu/fasta_www2/fasta_down.shtml "FASTA downloads")

   We use ssearch36 (a part of the FASTA suite of programs) to perform alignment and generate standardized alignment statistics.

* [hmmtop](http://www.enzim.hu/hmmtop/index.php "HMMTOP")

   For prediction of TransMembrane Segments, we utilize hmmtop.

## Workflow

1. evaluateAlignments.py

   The first step in the workflow is using the evaluateAlignments.py script to process the analyses performed to generate a a list of homologues by comparing a proteome against [TCDB](http://tcdb.org/ "TCDB Homepage"). The goal is to standardize the alignment statistics by using _ssearch36_.

   ```
   usage: evaluateAlignments.py [-h] [-i INFILE] [-of OUTFILE] [-od OUTDIR]

   A tool developed to standardize the alignment statistics used for comparative
   proteomic analysis in the Saier Lab at UCSD. Currently, protein sequences are
   acquired from BLAST databases using blastdbcmd and all alignments are
   performed using ssearch36.

   optional arguments:
      -h, --help            show this help message and exit
      -i INFILE, --infile INFILE
                            The path to the tsv file containing the results of a
                            proteome analysis
     -of OUTFILE, --outfile OUTFILE
                            The name for the file containing alignment statistics
                            (without the file extension), which will be place in
                            the output directory. Default is results
     -od OUTDIR, --outdir OUTDIR
                            The path to the directory where all the analysis files
                            will be output. Default is ./output
   ```
   The input format for the _infile_ (-i) is a tab-separated value (tsv) file with 3 columns in this order:
   | Query Accession | TCDB Protein Accession | TCDB ID |
   |-----------------|------------------------|---------|
   If you have a header in your file, please add a `#` character at the beginning of the line, so the program will skip the header.


2. createTables.py

   This is the script to create the master tables.
   ```
   usage: createTables.py [-h] [-i INPUT_DIRECTORY] [-of OUTFILE] [-od OUTDIR]

   A command line tool to process proteome analysis tables

   optional arguments:
     -h, --help            show this help message and exit
     -i INPUT_DIRECTORY, --input_directory INPUT_DIRECTORY
                           The path to the directory containing all the tsv files
                           containing analysis.
     -of OUTFILE, --outfile OUTFILE
                           The name of the final file containing the master
                           table.
     -od OUTDIR, --outdir OUTDIR
                           The path to the directory where all the analysis files
                           will be output.
   ```
   Formatting for the input files is as a tsv with the columns in the following:

   |#query | q_tms |  acc  |   s_tms |  tcid  |  evalue | pident | qcov  |  scov |
   |-------|-------|-------|---------|--------|---------|--------|-------|-------|

# Documentation for script : _evaluateAlignments.py_

## Summary
This program is intended to standardize the approach for determining the alignment statistics for proteome analysis projects. During proteome analysis, many different methodologies are used to assist in identifying potential transport proteins. In an effort to be able to extend potential homologous relationships to other proteomes, we use _ssearch36_ for all alignments so that all alignment statistics are calculated with the same parameters. We also, for additional information, run _hmmtop_, to calculate the predicted number of TransMembrane Segments (TMS) in all proteins in the analysis. As input, we expect a tsv file with the columns in the following order: the query accession (the NCBI accession of the protein that has been flagged to be potentially homologous to a TCDB protein), the accession of the TCDB protein that the query accession has been flagged to be similar to, and the corresponding TCID. As output, you will receive these fields, plus the percent identity of the alignment, the query coverage, and the subject coverage of the alignments.

## Contributors

Vasu Iddamsetty and Arturo Medrano-Soto

## Dependencies
The following need to be available to be able to run the program:

1. **Python 3.X**
   You can download Python 3 from the [official website](https://www.python.org/). The following modules are also required:

      a) Biopython 1.75
      b) run_hmmtop (included in the BioVx distribution)

2. **_blast+ 2.6.0 to 2.10.0_**  
   Other versions of blast may require minor adaptations. Visit the [download site](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download).

3. **_HMMTOP_**
   You can download HMMTOP from the [official website](http://www.enzim.hu/hmmtop).

4. **_ssearch36_**
   Available as part of the FASTA suite of programs from [UVA](https://fasta.bioch.virginia.edu/fasta_www2/fasta_down.shtml).

## Command Line Options
The following options are available:
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

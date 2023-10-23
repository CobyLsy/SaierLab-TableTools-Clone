# Documentation for script : _compareTranscriptomeAssignments.py_

## Summary
A program developed to aid in performing cross-transcriptome studies using the Transporter Classfication Database (TCDB). This program takes in multiple analysis files, previously processed by evaluateAlignments.py. It then creates a combined table that contains TCDB proteins and the most similar proteins (determined through the analysis) from each of the proteomes, along with relevant alignment statistics as calculated by evaluateAlignments. Currently, the ChEBI classifications we have used are fixed, as determined by manual analysis in the past, but we will improve this functionality in a future version of this script.

## Contributors

Vasu Iddamsetty and Arturo Medrano-Soto

## Dependencies
The following need to be available to be able to run the program:

1. **Python 3.X**
   You can download Python 3 from the [official website](https://www.python.org/). The following modules are also required:

      a) _libChEBIpy_ (can be dowloaded using *pip*)
      c) chebi_parser (included in the BioVx distribution)
      b) substrate (included in the BioVx distribution)


## Command Line Options
The following options are available:
```
usage: compareTranscriptomeAssignments.py [-h] [-i INPUT_DIRECTORY]
                                          [-of OUTFILE] [-od OUTDIR]

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

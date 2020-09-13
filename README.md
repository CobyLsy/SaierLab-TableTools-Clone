# Table-Tools
A set of tools for making tables for genome projects

## createTable.py
This is the script to create the master tables.
```
usage: createTables.py [-h] [-i INPUT_DIRECTORY] [-of OUTFILE] [-od OUTDIR]

A command line tool to process proteom analysis tables

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

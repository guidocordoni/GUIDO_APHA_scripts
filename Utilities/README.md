In this folder you will find bash and python scripts that may be useful to prepare the files for bioinformatic analysis. This folder is under development and more scripts will be added in future when a specific need that can be solved by a script is identified.

Scripts available:

1) columns_compare.py: It takes as an argument a file called list.txt (2 columns tab separated) and reports:
 - Entries in the first column
 - Entries in the second column
 - Entries present in both columns
 - Entries missing from first column
 - Enties missing from second column
 As an example we used this to check if a list of samples in a spreadsheet have been all sequenced (i.e. creating a column from the folder containing the assembled sequences (ls *.fasta > sequences.txt)

2) bulk_remove_brackets: does what it says, remove brackets from sequences (or other files) names.

3) raw_seq_copier: Copy raw sequences R1 and R2 from different folders to a folder of choice (modify the script with destination folder). It takes as an argument a tab separated file called list.txt where in the first column you put all your samples (just the names not all sequence name i.e. for sample1_R1_001.fastq.gz and sample1_R1_001.fastq.gz the first column will contain just sample1), the second column contains the path.

4) This script take the first 1000 sequences from a set of fastq.gz sequences and save them in a folder (REDUCED_SEQ) creating fastq.gz files that have the same names of the original ones. You can modify the value 1000 below to the desidered number of sequences needed.
Use this script to generate short sequences for testing pipelines or scripts on your personal SCE avoiding incurring in the costs of bigger SCE machines.

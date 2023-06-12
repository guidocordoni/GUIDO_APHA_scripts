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

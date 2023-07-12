#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 14:18:39 2023

@author: guidocordoni
"""
# Removes specific sequences from a multifasta file 
from Bio import SeqIO

# Specify the input and output file paths
input_file = "20230322_core_full.fasta" #insert input multifasta here
output_file = "20230322_core_full.fasta_no_outliers.fasta" #insert output multifasta here

# Specify the identifiers of the sequences to remove
sequences_to_remove = ["IS12-14772", "IS12-14533", "ERR10359644", "ERR10360925", "ERR10359647", "ERR10360276", "ERR10360735"] #Insert the sequences to exclude here

# Open the input file and filter sequences
sequences = []
with open(input_file, "r") as file:
    for record in SeqIO.parse(file, "fasta"):
        if record.id not in sequences_to_remove:
            sequences.append(record)

# Write the filtered sequences to the output file
with open(output_file, "w") as file:
    SeqIO.write(sequences, file, "fasta")

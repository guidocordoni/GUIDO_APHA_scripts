#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 15:21:25 2023

@author: guidocordoni
"""
#it cleans from a multifasta file all sequences starting with XXX.
from Bio import SeqIO

# Specify the input and output file paths
input_file = "clean_full.fasta" #insert the input name
output_file = "clean_without_ERR.fasta" #insert the output name

# Open the input file and filter sequences
sequences = []
with open(input_file, "r") as file:
    for record in SeqIO.parse(file, "fasta"):
        if not record.id.startswith("ERR"): #change "ERR" with the root of your sample name (in IS12, IEC etc.)
            sequences.append(record)

# Write the filtered sequences to the output file
with open(output_file, "w") as file:
    SeqIO.write(sequences, file, "fasta")

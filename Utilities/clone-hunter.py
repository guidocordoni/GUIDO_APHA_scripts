#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 11:32:14 2023

@author: guidocordoni
"""
#It takes a square matrix generated by snp-dist and find all the couples with a difference in snps <=20
#It will save on a file clones.txt
#REMEMBER to remove the content of the first cell (snpdist-ver.xx) but keep the TAB

import pandas as pd

matrix_file = "dist_noERR_and_outliers.txt"  # Replace with the actual file path

# Load the matrix from the file using pandas
matrix_df = pd.read_csv(matrix_file, sep="\t", index_col=0)

# Find couples with a distance <= 20
couples_df = matrix_df[matrix_df <= 20].stack().reset_index() #you can change the value <=20 according to the bacteria that you are investigating
couples_df.columns = ["Clone1", "Clone2", "Distance"]

# Filter out duplicates and self-identity couples
couples_df = couples_df[couples_df["Clone1"] < couples_df["Clone2"]]

couples = couples_df[["Clone1", "Clone2", "Distance"]].values.tolist()

# Save the list of couples with distances to a file
output_file = "clones.txt"

with open(output_file, "w") as file:
    for couple in couples:
        file.write(f"{couple[0]}\t{couple[1]}\t{couple[2]}\n")

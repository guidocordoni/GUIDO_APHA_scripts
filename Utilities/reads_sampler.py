#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 11:42:31 2023

@author: guido.cordoni@apha.gov.uk
"""
# This script is currently setted to take 1000 sequences randomly selected using seqtk and multithread.  It takes fastq.gz files from an input folder of choice and save the reduced fastq.gz files in a folder of choice. The reduced files will have the same names of the original ones.
#You can modify the value 1000 below to the desidered number of sequences needed.
#Use this script to generate short sequences for testing pipelines or scripts on your personal SCE avoiding incurring in the costs of bigger SCE machines.
#Usage: python -i input_folder -o output folder. Use -h for help. 
#Made by Guido Cordoni guido.cordoni@apha.gov.uk
import os
import sys
import subprocess
import argparse
import concurrent.futures

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Reduce sequences using seqtk.")
parser.add_argument("-i", "--input", help="Input folder path containing fastq.gz files.", required=True)
parser.add_argument("-o", "--output", help="Output folder path for saving reduced sequences.", required=True)
args = parser.parse_args()

# Function to process a single fastq.gz file
def process_file(file):
    # Construct the input and output file paths
    input_file = os.path.join(args.input, file)
    output_file = os.path.join(args.output, file)

    # Run seqtk to sample 1000 sequences from the input file and save it to the output file
    subprocess.run(["seqtk", "sample", "-s100", input_file, "1000"], stdout=open(output_file, "w"), check=True)

# Get a list of fastq.gz files in the input folder
fastq_files = [file for file in os.listdir(args.input) if file.endswith(".fastq.gz")]

# Create the output folder if it doesn't exist
os.makedirs(args.output, exist_ok=True)

# Process the fastq.gz files in parallel using multithreading
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_file, fastq_files)

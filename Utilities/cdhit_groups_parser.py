#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 11:07:01 2023

@author: guidocordoni
"""

def parse_cdhit_output(cluster_file, sequence_file, output_file):
    # Read the cluster output file
    clusters = {}
    with open(cluster_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('>Cluster'):
                cluster_num = int(line.split()[1])
            else:
                sequence_id = line.split('>')[1].split('...')[0]
                clusters[sequence_id] = cluster_num

    # Modify the clustered sequence file to include cluster numbers
    with open(sequence_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if line.startswith('>'):
                sequence_id = line.strip().lstrip('>')
                if sequence_id in clusters:
                    cluster_num = clusters[sequence_id]
                    f_out.write(f">{cluster_num}\n")
                else:
                    f_out.write(line)
            else:
                f_out.write(line)

# Usage example
cluster_file = 'cd-hit_output.clstr'
sequence_file = 'cd-hit_output.aln'
output_file = 'output_with_clusters.aln'
parse_cdhit_output(cluster_file, sequence_file, output_file)


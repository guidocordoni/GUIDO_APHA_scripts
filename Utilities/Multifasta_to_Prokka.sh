#!/bin/bash
# Takes a multifasta file (i.e. Snippy full genome file) and run Procca on each sequence. Saves results in separated folders named after the sequences names.
# Path to the multifasta file
genome_multifasta="your/path/clean.full.fasta" #update here

# Output directory for Prokka annotations
output_dir="your/path/prokka_results" #update here

# Create the output directory if it doesn't exist
mkdir -p $output_dir

# Extract sample names from FASTA headers and iterate through them
grep ">" $genome_multifasta | sed 's/>//' | while read sample_name; do
    echo "Annotating sample: $sample_name"
    mkdir -p $output_dir/$sample_name
    prokka $genome_multifasta --outdir $output_dir/$sample_name --prefix $sample_name --force
done

echo "Genome annotation completed."

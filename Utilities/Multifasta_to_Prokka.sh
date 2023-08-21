#!/bin/bash
# Takes a multifasta file (i.e. Snippy full genome file) and run Procca on each sequence. Saves results in separated folders named after the sequences names.
# Path to the multifasta file
genome_multifasta="your/path/clean.full.fasta" #update here

# Output directory for Prokka annotations
output_dir="your/path/prokka_results" #update here

# Create the output directory if it doesn't exist
mkdir -p $output_dir

# Iterate through each sequence in the multifasta file
while read -r line; do
    if [[ $line =~ ^\> ]]; then
        if [[ -n $sample_dir ]]; then
            # Run Prokka on the previous sample
            sample_name=$(basename "$sample_fasta" .fasta)
            prokka "$sample_fasta" --outdir "$sample_dir/$sample_name.prokka" --prefix "$sample_name" --debug
        fi
        sample_name=$(echo $line | sed 's/^>//')
        sample_dir="$output_dir/$sample_name"
        echo "Annotating sample: $sample_name"
        mkdir -p $sample_dir
        sample_fasta="$sample_dir/$sample_name.fasta"
        echo $line > "$sample_fasta"
    else
        echo $line >> "$sample_fasta"
    fi
done < "$genome_multifasta"

# Run Prokka on the last sample
if [[ -n $sample_dir ]]; then
    sample_name=$(basename "$sample_fasta" .fasta)
    prokka "$sample_fasta" --outdir "$sample_dir/$sample_name.prokka" --prefix "$sample_name" --force --debug
fi

echo "Genome annotation completed."

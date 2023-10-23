#!/bin/bash

#Download Illumina fastq.gz from SRA. Modify the Organism to search (Enterococcus cecorum here), the projects to exclude (Err here) and the number of cores to use (-p12 here)

# Output directory
output_dir="downloaded_sequences"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Search for SRA accessions for "Enterococcus cecorum" Illumina raw reads
esearch -db sra -query "Enterococcus cecorum[Organism] AND illumina[Platform]" | \
efetch -format runinfo | \
cut -d ',' -f 1 | \
tail -n +2 | \
#If activated the line below will skip all the sequences starting for ERR. Modify ERR with the project suffix that you don't want to download 
#grep -v '^ERR' | \ 
#set below -p 12 according to your machine's core number
xargs -I{} -P 12 -n 1 bash -c 'fastq-dump --split-files --gzip --outdir "$1" "$2" && echo "Downloaded raw reads for $2"' _ "$output_dir" {}


#!/bin/bash
# This script copy raw sequences from different folders to a folder of choice. Ptovide a tab separated file with two columns :sample name and path. 



# Destination folder
destination_folder="/home/guidocordoni/fsx/ranch-52/PATHSAFE_raw_meat/raw_seq"


# Read list.txt file line by line
while IFS=$'\t' read -r sample_name file_path
do
    # Construct the full file names
    r1_file="$sample_name"_S*_R1_001.fastq.gz
    r2_file="$sample_name"_S*_R2_001.fastq.gz

    # Find the R1 file in the source folder
    source_r1_files=("$file_path"/$r1_file)
    num_r1_files=${#source_r1_files[@]}
    if [[ $num_r1_files -eq 1 ]]; then
        # Copy the R1 file to the destination folder
        cp "${source_r1_files[0]}" "$destination_folder/$sample_name-R1.fastq.gz"
        echo "Copied R1 file for sample $sample_name"
    elif [[ $num_r1_files -eq 0 ]]; then
        echo "R1 file not found for sample $sample_name"
    else
        echo "Multiple R1 files found for sample $sample_name"
    fi

    # Find the R2 file in the source folder
    source_r2_files=("$file_path"/$r2_file)
    num_r2_files=${#source_r2_files[@]}
    if [[ $num_r2_files -eq 1 ]]; then
        # Copy the R2 file to the destination folder
        cp "${source_r2_files[0]}" "$destination_folder/$sample_name-R2.fastq.gz"
        echo "Copied R2 file for sample $sample_name"
    elif [[ $num_r2_files -eq 0 ]]; then
        echo "R2 file not found for sample $sample_name"
    else
        echo "Multiple R2 files found for sample $sample_name"
    fi

done < list.txt

echo "Copy process complete."




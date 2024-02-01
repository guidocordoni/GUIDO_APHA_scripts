#!/bin/bash

# List all Conda environments
environments=$(conda info --envs | grep -v "#" | awk '{print $1}' | tail -n +3)

# Initialize output file
output_file="software.txt"
echo "" > "$output_file"

# Loop through each environment and append installed packages to the output file
for env in $environments
do
    echo "Environment: $env" >> "$output_file"
    (source activate $env && conda list) >> "$output_file"
    conda deactivate
done


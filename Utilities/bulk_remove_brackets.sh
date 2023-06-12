#!/bin/bash

# Get the list of files in the current directory
files=$(ls)

# Loop through each file
for file in $files; do
    # Remove brackets from the file name using parameter expansion
    new_name="${file//[()]/}"
    
    # Check if the file name has changed
    if [ "$file" != "$new_name" ]; then
        # Rename the file
        mv "$file" "$new_name"
        echo "Renamed file: $file -> $new_name"
    fi
done


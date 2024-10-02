#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_dir> <destination_dir>"
    exit 1
fi

# Set source and destination directories
source_dir=$(realpath "$1")
destination_dir=$(realpath "$2")

# Ensure both source and destination directories exist
if [ ! -d "$source_dir" ]; then
    echo "Source directory does not exist: $source_dir"
    exit 1
fi

if [ ! -d "$destination_dir" ]; then
    echo "Destination directory does not exist, creating: $destination_dir"
    mkdir -p "$destination_dir"
fi

# Loop over all subfolders in the source directory
cd $source_dir
for subfolder in ./*/; do
    if [ -d "$subfolder" ]; then
        echo "Processing folder: $subfolder"
        
        # Find and copy all *_eight.pdb files, preserving the folder structure
        find "$subfolder" -type f -name '*_ten.pdb' -exec cp --parents {} "$destination_dir" \;
        
        # Find and copy all msas/chain_id_map.json files, preserving the folder structure
        find "$subfolder" -type f -path '*/msas/chain_id_map.json' -exec cp --parents {} "$destination_dir" \;
    fi
done

echo "Copy operation completed!"


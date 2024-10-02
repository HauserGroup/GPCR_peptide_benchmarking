#!/bin/bash

# Usage: ./copy_pdb_and_json.sh /path/to/source /path/to/target /path/to/folder_list.txt

# Check if three arguments are passed
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 source_directory target_directory folder_list.txt"
    exit 1
fi

# Set source and destination directories
SOURCE_DIR=$(realpath "$1")
TARGET_DIR=$(realpath "$2")
FOLDER_LIST="/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/tournament_benchmark/model_names.txt"

# Check if folder list file exists
if [ ! -f "$FOLDER_LIST" ]; then
    echo "Error: File $FOLDER_LIST not found!"
    exit 1
fi

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

cd $SOURCE_DIR

# Loop over each subfolder name from the text file
while IFS= read -r SUBFOLDER_NAME; do
    # Find all PDB files containing "___" in subfolders matching the name
    find "./$SUBFOLDER_NAME" -type f -name '*___*.pdb' -exec cp --parents {} "$TARGET_DIR" \;

    # Find all 'chain_id_map.json' files under 'msas/' directories in subfolders matching the name
    find "./$SUBFOLDER_NAME" -type f -path '*/msas/chain_id_map.json' -exec cp --parents {} "$TARGET_DIR" \;
done < "$FOLDER_LIST"

echo "Copy process completed!"


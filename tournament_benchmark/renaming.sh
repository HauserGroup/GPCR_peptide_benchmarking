#!/bin/bash

# Usage: ./rename_folders.sh /path/to/parent_directory

# Check if directory is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 /path/to/parent_directory"
    exit 1
fi

PARENT_DIR=$1

# Check if the provided path is a directory
if [ ! -d "$PARENT_DIR" ]; then
    echo "Error: $PARENT_DIR is not a valid directory!"
    exit 1
fi

# Loop through all subfolders in the parent directory
for DIR in "$PARENT_DIR"/*/; do
    # Remove the trailing slash from directory name
    DIR=${DIR%/}

    # Extract the folder name
    FOLDER_NAME=$(basename "$DIR")

    # Check if the folder contains "_human___"
    if [[ "$FOLDER_NAME" == *_human___* ]]; then
        # Rename the folder by replacing everything after "_human___" with "_one_to_one"
        NEW_NAME=$(echo "$FOLDER_NAME" | sed 's/_human___.*/_one_to_one/')

        # Perform the renaming
        mv "$DIR" "$PARENT_DIR/$NEW_NAME"

        echo "Renamed: $FOLDER_NAME -> $NEW_NAME"
    fi
done

echo "Renaming process completed!"


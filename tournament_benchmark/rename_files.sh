#!/bin/bash

# Usage: ./rename_files.sh /path/to/parent_directory

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

# Find all files recursively in the parent directory
find "$PARENT_DIR" -type f | while read FILE; do
    # Extract the base name of the file
    FILENAME=$(basename "$FILE")

    # Extract the file extension (everything after the last '.')
    EXTENSION="${FILENAME##*.}"

    # Extract the file name without the extension
    BASENAME="${FILENAME%.*}"

    # Check if the file name (excluding extension) contains "_human___"
    if [[ "$BASENAME" == *_human___* ]]; then
        # Rename the file by replacing everything after "_human___" with "_one_to_one", preserving the extension
        NEW_BASENAME=$(echo "$BASENAME" | sed 's/_human___.*/_one_to_one/')

        # Construct the new file name with the same extension
        NEW_FILENAME="${NEW_BASENAME}.${EXTENSION}"

        # Construct the new file path
        NEW_FILEPATH=$(dirname "$FILE")/"$NEW_FILENAME"

        # Perform the renaming
        mv "$FILE" "$NEW_FILEPATH"

        echo "Renamed: $FILENAME -> $NEW_FILENAME"
    fi
done

echo "File renaming process completed!"


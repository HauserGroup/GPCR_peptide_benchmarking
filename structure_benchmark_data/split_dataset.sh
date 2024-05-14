#!/bin/bash

# Directory containing the files
input_dir=$1
cd $input_dir

# List all files
files=(*)

# Calculate the number of files and the midpoint
total_files=${#files[@]}
half_point=$((total_files / 2))

# Create the first archive with the first half of files
tar -czf part1.tar.gz "${files[@]:0:half_point}"

# Create the second archive with the second half of files
tar -czf part2.tar.gz "${files[@]:half_point}"

echo "Created two archives with approximately equal number of files."

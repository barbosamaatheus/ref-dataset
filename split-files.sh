#!/bin/bash
# Script to split large files into parts of maximum 50MB.
# It searches recursively for files larger than 50MB,
# splits them into chunks, prints the file name, and then removes the original file.

# Define the size threshold (50MB)
SIZE_THRESHOLD="50M"

# Find files larger than 50MB and process each one
find . -type f -size +${SIZE_THRESHOLD} | while read -r FILE; do
    if [[ -f "$FILE" ]]; then
        echo "Splitting file: $FILE"
        # Split the file into parts with 50MB each.
        # The parts will be named as: originalname.part_aa, originalname.part_ab, etc.
        split -b ${SIZE_THRESHOLD} "$FILE" "${FILE}.part_"
        # Remove the original file after splitting
        rm "$FILE"
        echo "Original file removed: $FILE"
    fi
done
#!/bin/bash
# Script to recombine split file parts and reconstruct the original files.
# It searches recursively for files ending with ".part_aa" (indicating the first part),
# concatenates all corresponding parts in order, and then removes the split parts.

# Find all files that are the first part of a split (ending with .part_aa)
find . -type f -name "*.part_aa" | while read -r PART_FILE; do
    # Get the base file name by removing the .part_aa suffix
    BASE_FILE="${PART_FILE%.part_aa}"
    echo "Reconstructing file: $BASE_FILE"

    # Concatenate all parts belonging to the base file in lexicographic order
    cat "${BASE_FILE}.part_"* > "$BASE_FILE"

    # Remove the split parts after reconstruction
    rm "${BASE_FILE}.part_"*
    echo "File reconstructed: $BASE_FILE"
done

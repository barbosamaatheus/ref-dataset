#!/usr/bin/env bash
#
# Usage:
#   ./git_push_in_batches.sh [directory] [batch_size]
#
# Example:
#   ./git_push_in_batches.sh . 100
#
# Notes:
# - By default, if you don't provide arguments, it will use the current directory (.) and a batch size of 50 files.

# Parameters
DIRECTORY="${1:-.}"      # Target directory (default = current directory)
BATCH_SIZE="${2:-50}"    # Number of files to add before each commit (default = 50)

# Counters
COUNTER=0
CHUNK=1

# List all files (recursively) in the directory.
# If you need to filter certain extensions, add parameters to find (e.g., -name "*.pdf").
FILES=$(find "$DIRECTORY" -type f)

# Make sure you are in the correct Git repository:
# Before running, do `cd /path/to/your/repo` and `git status` to check it.

for FILE in $FILES; do
  # Add the file to the Git index
  git add "$FILE"
  ((COUNTER++))

  # Once the batch is reached, commit and push
  if [ "$COUNTER" -ge "$BATCH_SIZE" ]; then
    git commit -m "Batch commit #$CHUNK"
    git push
    COUNTER=0
    ((CHUNK++))
  fi
done

# If there are still uncommitted files (the last batch is smaller than BATCH_SIZE)
if [ "$COUNTER" -gt 0 ]; then
  git commit -m "Final commit (incomplete batch)"
  git push
fi

echo "Process complete!"

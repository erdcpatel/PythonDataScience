#!/bin/bash

# Define the file and the name for the MD5 storage file
file="your_file.txt"
md5file="md5.txt"

# Calculate the MD5 checksum of the current file
current_md5=$(md5sum "$file" | cut -d ' ' -f 1)

# Check if the MD5 file exists
if [ -f "$md5file" ]; then
  # Read the stored MD5 from the file
  stored_md5=$(cat "$md5file")

  # Compare the current and stored MD5 checksums
  if [ "$current_md5" = "$stored_md5" ]; then
    echo "MD5 is the same as before: $current_md5"
  else
    echo "MD5 is different: $stored_md5 (before) vs. $current_md5 (now)"
    # Update the MD5 file with the current MD5
    echo "$current_md5" > "$md5file"
  fi
else
  # The MD5 file doesn't exist, so create it and store the current MD5
  echo "MD5 file does not exist. Creating..."
  echo "$current_md5" > "$md5file"
fi

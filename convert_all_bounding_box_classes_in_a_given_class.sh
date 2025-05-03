#!/bin/bash

# Get the directory path from the user (optional)
# Uncomment the next line and modify the prompt if you want to prompt for a directory
# read -p "Enter the directory path: " directory

# Use the current directory by default (if no input provided)
directory=${1:-$PWD}

GIVEN_CLASS_NUMBER=2

# Check if directory exists
if [ ! -d "$directory" ]; then
  echo "Error: Directory '$directory' does not exist."
  exit 1
fi

# Loop through all files in the directory

for filename in "$directory"/*.txt; do
  # Check if it's actually a file (avoid hidden files, etc.)
  if [ -f "$filename" ]; then

    # Use sed to replace the first character of each line
      sed -i "s/^./$GIVEN_CLASS_NUMBER/" "$filename"
      echo "Replaced first character of each line in '$filename' with '\$GIVEN_CLASS_NUMBER'"
   
    
  fi
done

echo "Finished processing files in '$directory'"

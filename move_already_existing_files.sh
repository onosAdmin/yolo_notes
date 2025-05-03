
To extract and move all files that are present in a folder and also in reference foder and move them to a target folder.



#for file in /path/to/source/*; do [ -f "$file" ] && filename=$(basename "$file") && [ -f "/path/to/reference/$filename" ] && mv "$file" "/path/to/target/$filename" && echo "Moved: $filename"; done



#!/bin/bash

# Check if all arguments are provided
#if [ $# -ne 3 ]; then
#    echo "Usage: $0 <source_folder> <reference_folder> <target_folder>"
#    exit 1
#fi

SOURCE_FOLDER="/media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/train/labels/"
REFERENCE_FOLDER="/media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/dataset_source/Lego.v1i.yolov11/test/labels/"
TARGET_FOLDER="/tmp/copied"

# Check if folders exist
if [ ! -d "$SOURCE_FOLDER" ]; then
    echo "Error: Source folder '$SOURCE_FOLDER' does not exist"
    exit 1
fi

if [ ! -d "$REFERENCE_FOLDER" ]; then
    echo "Error: Reference folder '$REFERENCE_FOLDER' does not exist"
    exit 1
fi

# Create target folder if it doesn't exist
mkdir -p "$TARGET_FOLDER"

echo "Checking files from '$SOURCE_FOLDER' against '$REFERENCE_FOLDER'"
echo "Matches will be moved to '$TARGET_FOLDER'"

# Counter for moved files
moved_count=0

# Loop through each file in the source folder
for source_file in "$SOURCE_FOLDER"/*; do
    # Skip if it's a directory
    if [ -d "$source_file" ]; then
        continue
    fi
    
    # Get just the filename without the path
    filename=$(basename "$source_file")
    
    # Check if the file exists in the reference folder
    if [ -f "$REFERENCE_FOLDER/$filename" ]; then
        # Move the file to the target folder
        mv "$source_file" "$TARGET_FOLDER/$filename"
        echo "Moved: $filename"
        ((moved_count++))
    fi
done

echo "Done! Moved $moved_count files."

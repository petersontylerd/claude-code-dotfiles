#!/bin/bash

# Script to copy Codex CLI dotfiles to a destination directory
# Usage: ./copy-dotfiles.sh <source_directory> <destination_directory>

set -e  # Exit on any error

# Check if correct number of arguments provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <source_directory> <destination_directory>"
    echo "Example: $0 /home/ubuntu/repos/codex-dotfiles /path/to/destination"
    exit 1
fi

SOURCE_DIR="$1"
DEST_DIR="$2"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist"
    exit 1
fi

# Create destination directory if it doesn't exist
if [ ! -d "$DEST_DIR" ]; then
    echo "Creating destination directory: $DEST_DIR"
    mkdir -p "$DEST_DIR"
fi

echo "Copying Codex CLI dotfiles from '$SOURCE_DIR' to '$DEST_DIR'"

# List of files and directories to copy
FILES_TO_COPY=(
    "AGENTS.md"
    "MASTER_AGENTS.md"
)

DIRS_TO_COPY=(
    ".codex/docs"
)

# Copy individual files
echo "Copying files..."
for file in "${FILES_TO_COPY[@]}"; do
    source_file="$SOURCE_DIR/$file"
    if [ -f "$source_file" ]; then
        echo "  Copying $file"
        cp "$source_file" "$DEST_DIR/"
    else
        echo "  Warning: File '$source_file' not found, skipping"
    fi
done

# Copy directories and their contents
echo "Copying directories..."
for dir in "${DIRS_TO_COPY[@]}"; do
    source_dir="$SOURCE_DIR/$dir"
    dest_path="$DEST_DIR/$dir"
    
    if [ -d "$source_dir" ]; then
        echo "  Copying directory $dir"
        # Create parent directory structure if needed
        mkdir -p "$(dirname "$dest_path")"
        # Copy directory and all contents recursively
        cp -r "$source_dir" "$dest_path"
    else
        echo "  Warning: Directory '$source_dir' not found, skipping"
    fi
done

echo "Copy operation completed successfully!"
echo "Files and directories copied to: $DEST_DIR"

# Optional: List what was copied
echo ""
echo "Contents of destination directory:"
ls -la "$DEST_DIR"
if [ -d "$DEST_DIR/.codex" ]; then
    echo ""
    echo "Contents of .codex directory:"
    ls -la "$DEST_DIR/.codex"
fi
#!/usr/bin/env bash
# ABOUTME: Downloads Claude Code dotfiles from remote GitHub repository and installs them to specified project directory
# Used by local create_github_repo.sh when --claude-code flag is provided

set -euo pipefail

# ---------------------------
# Configuration
# ---------------------------
REMOTE_REPO="https://github.com/petersontylerd/claude-code-dotfiles"
REMOTE_BRANCH="main"

# -----------
# Utilities
# -----------
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
log()  { printf "${GREEN}[INSTALL]${NC} %s\n" "$*"; }
oops() { printf "${RED}[ERROR]${NC} %s\n" "$*" >&2; exit 1; }

usage() {
  cat <<EOF
Usage: $(basename "$0") <destination_directory>

Arguments:
  destination_directory    Target directory to install Claude Code dotfiles

This script downloads the latest Claude Code dotfiles from:
$REMOTE_REPO (branch: $REMOTE_BRANCH)

Files installed:
  - CLAUDE.md
  - .mcp.json
  - .claude/commands/
  - .claude/docs/
  - .claude/templates/
EOF
}

# ---------------
# Parse arguments
# ---------------
[[ $# -ne 1 ]] && { usage; oops "Destination directory is required."; }
DEST_DIR="$1"

# ----------------
# Prereq checks
# ----------------
command -v curl >/dev/null || oops "curl not found."
command -v tar >/dev/null || oops "tar not found."

# ----------------
# Validate destination
# ----------------
if [[ ! -d "$DEST_DIR" ]]; then
  oops "Destination directory does not exist: $DEST_DIR"
fi

# ----------------
# Setup temporary directory
# ----------------
TEMP_DIR=$(mktemp -d)
cleanup() {
  if [[ -n "${TEMP_DIR:-}" && -d "$TEMP_DIR" ]]; then
    log "Cleaning up temporary directory: $TEMP_DIR"
    rm -rf "$TEMP_DIR"
  fi
}
trap cleanup EXIT

# ----------------
# Download from remote repository
# ----------------
log "Downloading Claude Code dotfiles from $REMOTE_REPO"
cd "$TEMP_DIR"

# Download repository as tarball
curl -L "$REMOTE_REPO/archive/refs/heads/$REMOTE_BRANCH.tar.gz" -o claude-dotfiles.tar.gz || oops "Failed to download repository"
tar -xzf claude-dotfiles.tar.gz || oops "Failed to extract repository"

SOURCE_DIR="$TEMP_DIR/claude-code-dotfiles-$REMOTE_BRANCH"

# ----------------
# Verify source files exist
# ----------------
if [[ ! -d "$SOURCE_DIR" ]]; then
  oops "Downloaded repository not found at: $SOURCE_DIR"
fi

# ----------------
# Copy files and directories
# ----------------
log "Installing Claude Code dotfiles to: $DEST_DIR"

# List of files and directories to copy (same as original script)
FILES_TO_COPY=(
    "CLAUDE.md"
    ".mcp.json"
)

DIRS_TO_COPY=(
    ".claude/commands"
    ".claude/docs"
    ".claude/templates"
)

# Copy individual files
log "Installing files..."
for file in "${FILES_TO_COPY[@]}"; do
    source_file="$SOURCE_DIR/$file"
    if [[ -f "$source_file" ]]; then
        log "  Installing $file"
        cp "$source_file" "$DEST_DIR/"
    else
        log "  Warning: File '$source_file' not found in remote repository, skipping"
    fi
done

# Copy directories and their contents
log "Installing directories..."
for dir in "${DIRS_TO_COPY[@]}"; do
    source_dir="$SOURCE_DIR/$dir"
    dest_path="$DEST_DIR/$dir"

    if [[ -d "$source_dir" ]]; then
        log "  Installing directory $dir"
        # Create parent directory structure if needed
        mkdir -p "$(dirname "$dest_path")"
        # Copy directory and all contents recursively
        cp -r "$source_dir" "$dest_path"
    else
        log "  Warning: Directory '$source_dir' not found in remote repository, skipping"
    fi
done

# ----------------
# Verify installation
# ----------------
log "Verifying installation..."
INSTALLED_COUNT=0

for file in "${FILES_TO_COPY[@]}"; do
    if [[ -f "$DEST_DIR/$file" ]]; then
        ((INSTALLED_COUNT++))
    fi
done

for dir in "${DIRS_TO_COPY[@]}"; do
    if [[ -d "$DEST_DIR/$dir" ]]; then
        ((INSTALLED_COUNT++))
    fi
done

if [[ $INSTALLED_COUNT -eq 0 ]]; then
    oops "No files were successfully installed"
fi

# ----------------
# Success
# ----------------
log "Claude Code dotfiles installation completed successfully!"
log "Installed $INSTALLED_COUNT items to: $DEST_DIR"
log ""
log "Available directories:"
if [[ -d "$DEST_DIR/.claude" ]]; then
    ls -la "$DEST_DIR/.claude"
fi
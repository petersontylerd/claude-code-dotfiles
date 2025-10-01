#!/bin/bash
# ABOUTME: Script to add codex-git-ops as a git submodule at the repository root
# and initialize it so it's accessible to Claude Code and/or Codex CLI.

set -e

# Change to repository root
cd "$(git rev-parse --show-toplevel)"

# Add the submodule
echo "Adding codex-git-ops as a submodule..."
git submodule add https://github.com/petersontylerd/codex-git-ops.git codex-git-ops

# Initialize and update the submodule
echo "Initializing and updating submodule..."
git submodule update --init --recursive

# Verify the submodule is populated
if [ -d "codex-git-ops/.git" ] || [ -f "codex-git-ops/.git" ]; then
    echo "✓ Submodule codex-git-ops successfully added and initialized"
    echo "✓ Contents are now accessible to Claude Code and/or Codex CLI"
else
    echo "✗ Error: Submodule initialization may have failed"
    exit 1
fi

echo ""
echo "Next steps:"
echo "  - Review the changes: git status"
echo "  - Commit the submodule: git commit -m 'Add codex-git-ops submodule'"

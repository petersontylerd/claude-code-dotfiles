#!/usr/bin/env bash
# Balanced, polyglot-friendly Python (uv) scaffold — updated pre-commit stages
# Usage:
#   create-uv-balanced <project-name> [--github] [--public] [--python 3.12] [--strict] [--base ~/repos]

set -euo pipefail

# ---------------------------
# Defaults
# ---------------------------
CREATE_GITHUB=false
PRIVATE_REPO=true
PY_VERSION="3.12"
STRICT=false
BASE_DIR="${HOME}/repos"

# -----------
# Utilities
# -----------
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
log()  { printf "${GREEN}[INFO]${NC} %s\n" "$*"; }
oops() { printf "${RED}[ERROR]${NC} %s\n" "$*" >&2; exit 1; }

usage() {
  cat <<EOF
Usage: $(basename "$0") <project-name> [--github] [--public] [--python X.Y] [--strict] [--base DIR]

Options:
  --github          Create and push a GitHub repo via 'gh'
  --public          Make the GitHub repo public (default private)
  --python X.Y      Python version to pin with uv (default ${PY_VERSION})
  --strict          Add modest ruff/mypy opinions (still reasonable)
  --base DIR        Parent directory for project (default ${BASE_DIR})
EOF
}

# ---------------
# Parse arguments
# ---------------
[[ $# -lt 1 ]] && { usage; oops "Project name is required."; }
PROJECT_NAME="$1"; shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --github) CREATE_GITHUB=true ;;
    --public) PRIVATE_REPO=false ;;
    --python) shift; PY_VERSION="${1:-$PY_VERSION}" ;;
    --strict) STRICT=true ;;
    --base)   shift; BASE_DIR="${1:-$BASE_DIR}" ;;
    -h|--help) usage; exit 0 ;;
    *) oops "Unknown option: $1" ;;
  esac
  shift || true
done

# ----------------
# Prereq checks
# ----------------
command -v uv  >/dev/null || oops "uv not found. See: https://docs.astral.sh/uv/"
command -v git >/dev/null || oops "git not found."
if $CREATE_GITHUB; then
  command -v gh >/dev/null || oops "GitHub CLI (gh) not found."
  gh auth status >/dev/null || oops "GitHub CLI is not authenticated (run 'gh auth login')."
fi

# ----------------
# Paths & guards
# ----------------
PROJECT_DIR="${BASE_DIR}/${PROJECT_NAME}"
[[ -e "$PROJECT_DIR" ]] && oops "Project already exists: $PROJECT_DIR"
mkdir -p "$BASE_DIR"

# ----------------
# Create project
# ----------------
log "Creating project at: ${PROJECT_DIR}"
cd "$BASE_DIR"
uv init "$PROJECT_NAME"
cd "$PROJECT_DIR"

# Pin Python
uv python pin "$PY_VERSION"

# Add dev-only tools (no runtime deps)
log "Adding dev tools (ruff, mypy, pre-commit, bandit, pip-audit)..."
uv add --group dev ruff mypy pre-commit bandit pip-audit

# Minimal, non-opinionated pyproject
log "Writing minimal pyproject tool sections..."
cat >> pyproject.toml <<EOF

[tool.ruff]
# Neutral: only help with version inference.
target-version = "py$(echo "$PY_VERSION" | tr -d .)"

[tool.mypy]
# Neutral: only declare Python version + ignore missing imports for low friction.
python_version = "${PY_VERSION}"
ignore_missing_imports = true
EOF

# Scoped, polyglot-friendly pre-commit with UPDATED STAGES
log "Creating .pre-commit-config.yaml..."
cat > .pre-commit-config.yaml <<'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff-format
        stages: [pre-commit]
        files: '\.py$'
      - id: ruff
        stages: [pre-commit]
        files: '\.py$'

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.2
    hooks:
      - id: mypy
        stages: [pre-commit]
        files: '\.py$'
        additional_dependencies: []

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.9
    hooks:
      - id: bandit
        stages: [pre-push]
        files: '\.py$'
        args: [-q, -r, .]

  - repo: https://github.com/pypa/pip-audit
    rev: v2.7.3
    hooks:
      - id: pip-audit
        stages: [pre-push]
        pass_filenames: false
EOF

# Polyglot-friendly .gitignore
log "Creating .gitignore..."
cat > .gitignore <<'EOF'
# Python
__pycache__/
*.pyc
.venv/
.uv/
.coverage
.pytest_cache/

# Node / Next.js
node_modules/
dist/
.next/
.out/

# Editors / OS
.vscode/
.DS_Store
EOF

# ----------------
# Git init & hooks
# ----------------
log "Initializing git and installing hooks..."
git init -q
git add .
git commit -q -m "chore: initial scaffold (uv + minimal tooling)"
uv run pre-commit install --install-hooks

# ----------------
# Optional GitHub
# ----------------
if $CREATE_GITHUB; then
  VISIBILITY=$($PRIVATE_REPO && echo "--private" || echo "--public")
  log "Creating GitHub repo ($VISIBILITY)..."
  gh repo create "$PROJECT_NAME" $VISIBILITY --source=. --push --description "$PROJECT_NAME"
fi

# ----------------
# Optional STRICT
# ----------------
if $STRICT; then
  log "Applying STRICT profile (modest, still common defaults)..."
  cat >> pyproject.toml <<'EOF'

# --- STRICT PROFILE (optional) ---
[tool.ruff.lint]
select = ["E","W","F","I","B","UP"]

[tool.mypy]
check_untyped_defs = true
warn_unused_ignores = true
EOF
  git add pyproject.toml
  git commit -q -m "chore: enable STRICT profile (ruff/mypy modest opinions)"
fi

# ----------------
# Finish
# ----------------
log "Done."
log "Next steps:"
log "  cd \"$PROJECT_DIR\""
log "  # Commit to trigger hooks; push triggers security/audit."
log "  # Add Node/Next.js under apps/web, dbt under analytics/dbt, etc., without interference."

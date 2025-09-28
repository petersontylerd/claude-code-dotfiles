#!/usr/bin/env -S uv run python

"""
ABOUTME: Validates all epic artifacts against the epic template schema
Ensures epic artifacts follow expected structure and have consistent ID naming
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple
import re

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def load_yaml_file(file_path: Path) -> Tuple[Dict[str, Any], List[str]]:
    """Load and parse a YAML file, returning content and any errors."""
    errors: List[str] = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
            return content or {}, errors
    except FileNotFoundError:
        errors.append(f"File not found: {file_path}")
        return {}, errors
    except yaml.YAMLError as e:
        errors.append(f"YAML parsing error: {e}")
        return {}, errors
    except Exception as e:
        errors.append(f"Unexpected error reading file: {e}")
        return {}, errors


def validate_structure(
    artifact: Dict[str, Any], template: Dict[str, Any], path: str = ""
) -> List[str]:
    """Recursively validate artifact structure against template."""
    errors: List[str] = []

    for key, template_value in template.items():
        current_path = f"{path}.{key}" if path else key

        if key not in artifact:
            errors.append(f"Missing required field: {current_path}")
            continue

        artifact_value = artifact[key]

        # Check if template value is a dict and needs recursive validation
        if isinstance(template_value, dict):
            if not isinstance(artifact_value, dict):
                errors.append(f"Field {current_path} should be a dictionary")
            else:
                errors.extend(
                    validate_structure(artifact_value, template_value, current_path)
                )

        # Check if template value is a list
        elif isinstance(template_value, list):
            if not isinstance(artifact_value, list):
                errors.append(f"Field {current_path} should be a list")
            elif template_value and isinstance(template_value[0], dict):
                # Validate list items against first template item if it's a dict
                for i, item in enumerate(artifact_value):
                    if isinstance(item, dict):
                        errors.extend(
                            validate_structure(
                                item, template_value[0], f"{current_path}[{i}]"
                            )
                        )

    return errors


def validate_epic_id_consistency(
    epic_file: Path, artifact: Dict[str, Any]
) -> List[str]:
    """Validate epic ID consistency between filename, directory, and content."""
    errors: List[str] = []

    # Extract epic ID from directory name
    epic_dir = epic_file.parent.name
    epic_id_match = re.search(r"epic-(E\d+)", epic_dir)
    if not epic_id_match:
        errors.append(f"Invalid epic directory name: {epic_dir}")
        return errors

    expected_epic_id = epic_id_match.group(1)

    # Check filename follows convention
    expected_filename = f"epic-{expected_epic_id}-name.yaml"
    if epic_file.name != expected_filename:
        errors.append(
            f"Epic filename should be {expected_filename}, got {epic_file.name}"
        )

    # Check epic_id in metadata
    if "metadata" in artifact and "epic_id" in artifact["metadata"]:
        actual_epic_id = artifact["metadata"]["epic_id"]
        if actual_epic_id != expected_epic_id:
            errors.append(
                f"Epic ID in metadata ({actual_epic_id}) doesn't match directory ({expected_epic_id})"
            )

    return errors


def find_epic_files() -> List[Path]:
    """Find all epic YAML files in the product-plan structure."""
    script_dir = Path(__file__).parent.parent.parent.parent
    product_plan_dir = script_dir / "product-plan" / "development"

    epic_files = []
    for epic_dir in product_plan_dir.glob("epic-E*"):
        if epic_dir.is_dir():
            epic_file = epic_dir / f"{epic_dir.name}-name.yaml"
            if epic_file.exists():
                epic_files.append(epic_file)

    return sorted(epic_files)


def validate_epics() -> bool:
    """Main validation function for all epic artifacts."""
    script_dir = Path(__file__).parent.parent.parent.parent
    template_path = (
        script_dir / "templates" / "product-plan" / "development" / "epic.yaml"
    )

    print(f"{BLUE}Validating epic artifacts...{RESET}")

    # Load template
    template, template_errors = load_yaml_file(template_path)
    if template_errors:
        print(f"{RED}Template errors:{RESET}")
        for error in template_errors:
            print(f"  - {error}")
        return False

    # Find all epic files
    epic_files = find_epic_files()
    if not epic_files:
        print(f"{RED}No epic files found{RESET}")
        return False

    print(f"Found {len(epic_files)} epic file(s)")

    all_errors: List[str] = []

    # Validate each epic file
    for epic_file in epic_files:
        print(f"  Validating {epic_file.name}...")

        # Load artifact
        artifact, artifact_errors = load_yaml_file(epic_file)
        if artifact_errors:
            all_errors.extend(
                [f"{epic_file.name}: {error}" for error in artifact_errors]
            )
            continue

        # Validate structure
        structure_errors = validate_structure(artifact, template)
        if structure_errors:
            all_errors.extend(
                [f"{epic_file.name}: {error}" for error in structure_errors]
            )

        # Validate ID consistency
        id_errors = validate_epic_id_consistency(epic_file, artifact)
        if id_errors:
            all_errors.extend([f"{epic_file.name}: {error}" for error in id_errors])

    # Report results
    if all_errors:
        print(f"{RED}Epic validation failed with {len(all_errors)} error(s):{RESET}")
        for error in all_errors:
            print(f"  - {error}")
        return False
    else:
        print(f"{GREEN}✓ All epic artifacts validation passed{RESET}")
        return True


if __name__ == "__main__":
    success = validate_epics()
    sys.exit(0 if success else 1)

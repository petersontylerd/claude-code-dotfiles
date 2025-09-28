#!/usr/bin/env -S uv run python

"""
ABOUTME: Validates development-considerations.yaml artifact against its template schema
Ensures the development-considerations artifact follows the expected structure and contains required fields
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple

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


def validate_development_considerations() -> bool:
    """Main validation function for development-considerations.yaml."""
    # Define paths
    script_dir = Path(__file__).parent.parent.parent.parent
    artifact_path = (
        script_dir / "product-plan" / "foundation" / "development-considerations.yaml"
    )
    template_path = (
        script_dir
        / "templates"
        / "product-plan"
        / "foundation"
        / "development-considerations.yaml"
    )

    print(f"{BLUE}Validating development-considerations.yaml...{RESET}")

    # Load template
    template, template_errors = load_yaml_file(template_path)
    if template_errors:
        print(f"{RED}Template errors:{RESET}")
        for error in template_errors:
            print(f"  - {error}")
        return False

    # Load artifact
    artifact, artifact_errors = load_yaml_file(artifact_path)
    if artifact_errors:
        print(f"{RED}Artifact errors:{RESET}")
        for error in artifact_errors:
            print(f"  - {error}")
        return False

    # Validate structure
    structure_errors = validate_structure(artifact, template)

    # Report results
    if structure_errors:
        print(f"{RED}Validation failed with {len(structure_errors)} error(s):{RESET}")
        for error in structure_errors:
            print(f"  - {error}")
        return False
    else:
        print(f"{GREEN}✓ development-considerations.yaml validation passed{RESET}")
        return True


if __name__ == "__main__":
    success = validate_development_considerations()
    sys.exit(0 if success else 1)

#!/usr/bin/env -S uv run python

"""
ABOUTME: Validates all feature artifacts against the feature template schema
Ensures feature artifacts follow expected structure and have consistent ID naming with parent epics
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


def validate_feature_id_consistency(
    feature_file: Path, artifact: Dict[str, Any]
) -> List[str]:
    """Validate feature ID consistency between filename, directory, and content."""
    errors: List[str] = []

    # Extract epic and feature IDs from directory structure
    feature_dir = feature_file.parent.name
    feature_match = re.search(r"feature-(E\d+)-(F\d+)", feature_dir)
    if not feature_match:
        errors.append(f"Invalid feature directory name: {feature_dir}")
        return errors

    expected_epic_id = feature_match.group(1)
    expected_feature_id = feature_match.group(2)

    # Check filename follows convention
    expected_filename = f"feature-{expected_epic_id}-{expected_feature_id}-name.yaml"
    if feature_file.name != expected_filename:
        errors.append(
            f"Feature filename should be {expected_filename}, got {feature_file.name}"
        )

    # Check feature_id and parent_epic in metadata
    if "metadata" in artifact:
        metadata = artifact["metadata"]

        if "feature_id" in metadata:
            actual_feature_id = metadata["feature_id"]
            if actual_feature_id != expected_feature_id:
                errors.append(
                    f"Feature ID in metadata ({actual_feature_id}) doesn't match directory ({expected_feature_id})"
                )

        if "parent_epic" in metadata:
            actual_parent_epic = metadata["parent_epic"]
            if actual_parent_epic != expected_epic_id:
                errors.append(
                    f"Parent epic in metadata ({actual_parent_epic}) doesn't match directory ({expected_epic_id})"
                )

    return errors


def find_feature_files() -> List[Path]:
    """Find all feature YAML files in the product-plan structure."""
    script_dir = Path(__file__).parent.parent.parent.parent
    product_plan_dir = script_dir / "product-plan" / "development"

    feature_files = []
    for epic_dir in product_plan_dir.glob("epic-E*"):
        if epic_dir.is_dir():
            features_dir = epic_dir / f"features-{epic_dir.name.split('-')[1]}"
            if features_dir.exists():
                for feature_dir in features_dir.glob("feature-E*-F*"):
                    if feature_dir.is_dir():
                        feature_file = feature_dir / f"{feature_dir.name}-name.yaml"
                        if feature_file.exists():
                            feature_files.append(feature_file)

    return sorted(feature_files)


def validate_features() -> bool:
    """Main validation function for all feature artifacts."""
    script_dir = Path(__file__).parent.parent.parent.parent
    template_path = (
        script_dir / "templates" / "product-plan" / "development" / "feature.yaml"
    )

    print(f"{BLUE}Validating feature artifacts...{RESET}")

    # Load template
    template, template_errors = load_yaml_file(template_path)
    if template_errors:
        print(f"{RED}Template errors:{RESET}")
        for error in template_errors:
            print(f"  - {error}")
        return False

    # Find all feature files
    feature_files = find_feature_files()
    if not feature_files:
        print(f"{RED}No feature files found{RESET}")
        return False

    print(f"Found {len(feature_files)} feature file(s)")

    all_errors: List[str] = []

    # Validate each feature file
    for feature_file in feature_files:
        print(f"  Validating {feature_file.name}...")

        # Load artifact
        artifact, artifact_errors = load_yaml_file(feature_file)
        if artifact_errors:
            all_errors.extend(
                [f"{feature_file.name}: {error}" for error in artifact_errors]
            )
            continue

        # Validate structure
        structure_errors = validate_structure(artifact, template)
        if structure_errors:
            all_errors.extend(
                [f"{feature_file.name}: {error}" for error in structure_errors]
            )

        # Validate ID consistency
        id_errors = validate_feature_id_consistency(feature_file, artifact)
        if id_errors:
            all_errors.extend([f"{feature_file.name}: {error}" for error in id_errors])

    # Report results
    if all_errors:
        print(f"{RED}Feature validation failed with {len(all_errors)} error(s):{RESET}")
        for error in all_errors:
            print(f"  - {error}")
        return False
    else:
        print(f"{GREEN}✓ All feature artifacts validation passed{RESET}")
        return True


if __name__ == "__main__":
    success = validate_features()
    sys.exit(0 if success else 1)

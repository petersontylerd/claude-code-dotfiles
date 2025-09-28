#!/usr/bin/env -S uv run python

"""
ABOUTME: Validates all user story artifacts against the user story template schema
Ensures user story artifacts follow expected structure and have consistent ID naming with parent features and epics
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


def validate_user_story_id_consistency(
    story_file: Path, artifact: Dict[str, Any]
) -> List[str]:
    """Validate user story ID consistency between filename, directory, and content."""
    errors: List[str] = []

    # Extract epic, feature, and user story IDs from filename
    story_match = re.search(r"user-story-(E\d+)-(F\d+)-(US\d+)", story_file.name)
    if not story_match:
        errors.append(f"Invalid user story filename: {story_file.name}")
        return errors

    expected_epic_id = story_match.group(1)
    expected_feature_id = story_match.group(2)
    expected_story_id = story_match.group(3)

    # Check user_story_id, parent_feature, and parent_epic in metadata
    if "metadata" in artifact:
        metadata = artifact["metadata"]

        if "user_story_id" in metadata:
            actual_story_id = metadata["user_story_id"]
            if actual_story_id != expected_story_id:
                errors.append(
                    f"User story ID in metadata ({actual_story_id}) doesn't match filename ({expected_story_id})"
                )

        if "parent_feature" in metadata:
            actual_parent_feature = metadata["parent_feature"]
            if actual_parent_feature != expected_feature_id:
                errors.append(
                    f"Parent feature in metadata ({actual_parent_feature}) doesn't match filename ({expected_feature_id})"
                )

        if "parent_epic" in metadata:
            actual_parent_epic = metadata["parent_epic"]
            if actual_parent_epic != expected_epic_id:
                errors.append(
                    f"Parent epic in metadata ({actual_parent_epic}) doesn't match filename ({expected_epic_id})"
                )

    return errors


def find_user_story_files() -> List[Path]:
    """Find all user story YAML files in the product-plan structure."""
    script_dir = Path(__file__).parent.parent.parent.parent
    product_plan_dir = script_dir / "product-plan" / "development"

    story_files = []
    for epic_dir in product_plan_dir.glob("epic-E*"):
        if epic_dir.is_dir():
            epic_id = epic_dir.name.split("-")[1]
            features_dir = epic_dir / f"features-{epic_id}"
            if features_dir.exists():
                for feature_dir in features_dir.glob(f"feature-{epic_id}-F*"):
                    if feature_dir.is_dir():
                        stories_dir = (
                            feature_dir
                            / f"user-stories-{epic_id}-{feature_dir.name.split('-')[2]}"
                        )
                        if stories_dir.exists():
                            for story_file in stories_dir.glob(
                                f"user-story-{epic_id}-*-US*-name.yaml"
                            ):
                                story_files.append(story_file)

    return sorted(story_files)


def validate_user_stories() -> bool:
    """Main validation function for all user story artifacts."""
    script_dir = Path(__file__).parent.parent.parent.parent
    template_path = (
        script_dir / "templates" / "product-plan" / "development" / "user-story.yaml"
    )

    print(f"{BLUE}Validating user story artifacts...{RESET}")

    # Load template
    template, template_errors = load_yaml_file(template_path)
    if template_errors:
        print(f"{RED}Template errors:{RESET}")
        for error in template_errors:
            print(f"  - {error}")
        return False

    # Find all user story files
    story_files = find_user_story_files()
    if not story_files:
        print(f"{RED}No user story files found{RESET}")
        return False

    print(f"Found {len(story_files)} user story file(s)")

    all_errors: List[str] = []

    # Validate each user story file
    for story_file in story_files:
        print(f"  Validating {story_file.name}...")

        # Load artifact
        artifact, artifact_errors = load_yaml_file(story_file)
        if artifact_errors:
            all_errors.extend(
                [f"{story_file.name}: {error}" for error in artifact_errors]
            )
            continue

        # Validate structure
        structure_errors = validate_structure(artifact, template)
        if structure_errors:
            all_errors.extend(
                [f"{story_file.name}: {error}" for error in structure_errors]
            )

        # Validate ID consistency
        id_errors = validate_user_story_id_consistency(story_file, artifact)
        if id_errors:
            all_errors.extend([f"{story_file.name}: {error}" for error in id_errors])

    # Report results
    if all_errors:
        print(
            f"{RED}User story validation failed with {len(all_errors)} error(s):{RESET}"
        )
        for error in all_errors:
            print(f"  - {error}")
        return False
    else:
        print(f"{GREEN}✓ All user story artifacts validation passed{RESET}")
        return True


if __name__ == "__main__":
    success = validate_user_stories()
    sys.exit(0 if success else 1)

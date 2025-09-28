#!/usr/bin/env -S uv run python

"""
ABOUTME: Master orchestration script for validating all product plan artifacts
Provides unified interface to run all validation scripts with filtering options
"""

import sys
import subprocess
from pathlib import Path
import argparse
import json
from typing import Dict, Tuple

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def run_validation_script(script_path: Path) -> Tuple[bool, str]:
    """Run a validation script and return success status and output."""
    try:
        result = subprocess.run(
            [str(script_path)], capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Script timed out after 30 seconds"
    except Exception as e:
        return False, f"Error running script: {e}"


def run_foundation_validation() -> Dict[str, Tuple[bool, str]]:
    """Run all foundation validation scripts."""
    script_dir = Path(__file__).parent
    foundation_dir = script_dir / "foundation"

    foundation_scripts = [
        "validate-brainstorm.py",
        "validate-vision.py",
        "validate-strategy.py",
        "validate-roadmap.py",
        "validate-personas.py",
        "validate-metrics.py",
        "validate-prd.py",
        "validate-development-considerations.py",
    ]

    results = {}
    for script_name in foundation_scripts:
        script_path = foundation_dir / script_name
        if script_path.exists():
            success, output = run_validation_script(script_path)
            results[script_name] = (success, output)
        else:
            results[script_name] = (False, f"Script not found: {script_path}")

    return results


def run_development_validation() -> Dict[str, Tuple[bool, str]]:
    """Run all development validation scripts."""
    script_dir = Path(__file__).parent
    development_dir = script_dir / "development"

    development_scripts = [
        "validate-epics.py",
        "validate-features.py",
        "validate-user-stories.py",
    ]

    results = {}
    for script_name in development_scripts:
        script_path = development_dir / script_name
        if script_path.exists():
            success, output = run_validation_script(script_path)
            results[script_name] = (success, output)
        else:
            results[script_name] = (False, f"Script not found: {script_path}")

    return results


def print_results(results: Dict[str, Tuple[bool, str]], verbose: bool = False) -> int:
    """Print validation results and return number of failures."""
    failures = 0

    for script_name, (success, output) in results.items():
        status_color = GREEN if success else RED
        status_text = "PASS" if success else "FAIL"

        print(f"{status_color}[{status_text}]{RESET} {script_name}")

        if verbose or not success:
            # Indent the output
            for line in output.strip().split("\n"):
                if line.strip():
                    print(f"    {line}")

        if not success:
            failures += 1

    return failures


def generate_json_report(
    foundation_results: Dict[str, Tuple[bool, str]],
    development_results: Dict[str, Tuple[bool, str]],
) -> Dict:
    """Generate JSON report of validation results."""

    def format_results(results):
        return {
            script: {"success": success, "output": output}
            for script, (success, output) in results.items()
        }

    return {
        "foundation": format_results(foundation_results),
        "development": format_results(development_results),
        "summary": {
            "foundation_passed": sum(
                1 for success, _ in foundation_results.values() if success
            ),
            "foundation_total": len(foundation_results),
            "development_passed": sum(
                1 for success, _ in development_results.values() if success
            ),
            "development_total": len(development_results),
            "overall_success": all(
                success
                for success, _ in {**foundation_results, **development_results}.values()
            ),
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Validate product plan artifacts")
    parser.add_argument(
        "--foundation-only",
        action="store_true",
        help="Only validate foundation artifacts",
    )
    parser.add_argument(
        "--development-only",
        action="store_true",
        help="Only validate development artifacts",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output for all scripts",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )

    args = parser.parse_args()

    if not args.json:
        print(f"{BLUE}Product Plan Validation Suite{RESET}")
        print("=" * 50)

    foundation_results = {}
    development_results = {}

    # Run foundation validation
    if not args.development_only:
        if not args.json:
            print(f"\n{BLUE}Foundation Artifacts:{RESET}")
        foundation_results = run_foundation_validation()
        if not args.json:
            foundation_failures = print_results(foundation_results, args.verbose)

    # Run development validation
    if not args.foundation_only:
        if not args.json:
            print(f"\n{BLUE}Development Artifacts:{RESET}")
        development_results = run_development_validation()
        if not args.json:
            development_failures = print_results(development_results, args.verbose)

    # Output results
    if args.json:
        report = generate_json_report(foundation_results, development_results)
        print(json.dumps(report, indent=2))
        return 0 if report["summary"]["overall_success"] else 1
    else:
        # Summary
        total_failures = (foundation_failures if foundation_results else 0) + (
            development_failures if development_results else 0
        )
        total_scripts = len(foundation_results) + len(development_results)
        total_passed = total_scripts - total_failures

        print(f"\n{BLUE}Summary:{RESET}")
        print(f"  Passed: {GREEN}{total_passed}{RESET}")
        print(f"  Failed: {RED}{total_failures}{RESET}")
        print(f"  Total:  {total_scripts}")

        if total_failures == 0:
            print(f"\n{GREEN}✓ All validations passed!{RESET}")
        else:
            print(f"\n{RED}✗ {total_failures} validation(s) failed{RESET}")

        return 0 if total_failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

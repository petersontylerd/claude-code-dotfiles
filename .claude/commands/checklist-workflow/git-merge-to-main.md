You are helping me finalize a completed feature branch in a git repository.

Preflight checks:
- Require a fresh `git status` before suggesting `git add -A`.
- Use atomic commit messages in `type(scope): description` form and ensure language-appropriate quality checks have passed before committing.
- Never suggest bypassing hooks (`--no-verify`, `--no-hooks`, `--no-pre-commit-hook`); if a hook fails, read the full output, identify the tool, explain the fix, apply it, rerun, and only commit once hooks pass.

All work on this feature branch is done: feature implementation, tests, and formatting checks are complete and passing. We are now ready to:

1. Commit any remaining changes for this feature
2. Merge this feature branch into `main`
3. Delete the feature branch once the merge is complete

**Critical constraint:** You are **forbidden** from running any git commands yourself.

Instead, you must:

* Only output the exact shell commands I should run, in the correct order, to:

  * commit the feature work (if needed),
  * merge the feature branch into `main`,
  * push any relevant branches, and
  * delete the feature branch (locally and remotely, if applicable).
* Format the commands so they are easy to copy and paste into a separate terminal that has the necessary permissions and network access.
* Use clear placeholders for any unknowns (e.g. `<feature-branch-name>`) and ask me for values you need.

After you provide the commands, I will run them.
I will then report back when they complete, and if there are any errors, I will paste the full terminal stdout/stderr for you to analyze.
When that happens, your job is to diagnose the issue and respond again **only** with updated or additional commands for me to run.

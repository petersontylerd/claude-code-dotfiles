---
description: Execute next task on initiative checklist currently in context
argument-hint: FEATURE_BRANCH=<feature_branch>
---
# `/execute-next-task`

You are in the **Execution Loop** phase of an initiative. Your job is to:

- Begin executing the *Recommended next subtask* immediately.
- If the *Recommended next subtask* is unclear, select the next most appropriate checklist item based on *Recommended next subtask* in prior response or priority/dependency ordering in checklist. Confirm your selection with the user.
- Plan it briefly.
- Execute it using tools and file edits.
- Validate results.
- Update the checklist and notes.

You must **favor concrete action** over mere description whenever environment constraints allow, and you must execute **exactly one checklist subtask per invocation** (do not begin multiple open items simultaneously).

---

## 1. Select and Understand the Next Task

1. Choose the next task according to:
   - First, default to the *Recommended next subtask* provided within the previous response, **or**
   - If prior response did not recommend a next best task, fall back to priority and dependency ordering in the checklist:
     - Prefer the highest-priority open (`[ ]`) item that is not annotated as blocked and that best advances the North Star / Goals.
   - If the chosen item is `[VALIDATE]`, confirm every referenced `[IMPLEMENT]` task is complete; otherwise, mark the validation as blocked and switch to the earliest incomplete `[IMPLEMENT]` it depends on.
2. Restate the chosen task in your own words:
   - Include its ID, prefix (e.g., `[IMPLEMENT]`), and its Major Task.
   - If the subtask scope is broad or ambiguous (e.g., “apply docstrings across modules”), first decompose it into concrete sub-subtasks (and sub-sub-subtasks if needed) scoped to specific directories/files/themes with explicit validation commands. Add these to the checklist, keep IDs/prefixes stable, and select the first new child to execute in this invocation. Do not proceed with code changes until this breakdown exists.
3. Verify you are on `$FEATURE_BRANCH` before executing: check the current branch (e.g., `git branch --show-current`). If the branch differs, stop and ask the user to switch before proceeding.
4. Confirm definition of done:
   - Files to touch.
   - Expected behavior.
   - Tests or checks to run.
   - On correct feature branch
   - If any item is unknown, stop and ask the user to supply it before proceeding.

Ask for clarification if anything is ambiguous.

---

## 2. Micro-Plan with `sequential-thinking`

1. Use **Sequential Thinking** to draft a 3–7 step micro-plan:
   - Context gathering.
   - Design decisions (if any).
   - Note any decomposition work already added to the checklist in Step 1; only reference it here, do not restate or duplicate instructions.
   - File edits with `serena`.
   - Tests/validation commands.
   - Checklist/notes updates.
2. sanity-check the plan:
   - Does it respect directory/test constraints?
   - Does it keep scope tight for this one task?

Do not skip this step for non-trivial tasks.
If external APIs or libraries are involved, plan a `context7` lookup and record key findings in Notes & Learnings.

---

## 3. Execute with Tools (Prefer Doing over Saying)

Follow your micro-plan step-by-step:

1. Use `serena` to inspect and edit relevant files.
2. When changing code or prompts:
   - Make small, focused edits.
   - Respect repo style.
   - For any new or modified Python functions or classes, add or update a Google-style docstring that documents `Args`, `Returns`, and `Raises` (or state “None” explicitly); treat missing docstrings as an incomplete change.
   - Work only inside the repo and relevant subpaths; use `apply_patch` (preferred) or `serena` file edits; only create/overwrite files when necessary.
   - For discovery, use shell tools scoped to the task (`rg --files`, `ls`, `find`, `rg pattern path`).
   - If you decomposed a broad task, ensure the new sub-subtasks from Step 1 are already in the checklist before execution; after execution, only mark status/results—do not duplicate updates.

### Google-style docstring quick example
```py
def fetch_user_profile(user_id: str, include_inactive: bool = False) -> dict:
    """Fetch a user profile from the data store.

    Args:
        user_id (str): Unique identifier of the user.
        include_inactive (bool, optional): Include inactive/soft-deleted users. Defaults to False.

    Returns:
        dict: Profile data, e.g. {"id": "12345", "name": "Jane Doe", "is_active": True}.

    Raises:
        ValueError: If user_id is empty.
        UserNotFoundError: If no user exists.
    """
```

3. When you need to run commands (tests, linters, scripts):
   - Attempt them if allowed by the environment.
   - If blocked by network/permissions/timeout:
     - Stop and produce **“Commands for User to Run”** section in the interactive terminal with:
       - Exact commands.
       - Expected behavior.
     - What logs/output you need back.
     - Mark the task as `blocked` in your narrative and in the checklist update plan.
     - Wait for the user to provide the necessary input. Then, evaluate it, update the checklist, and continue.

Avoid repeatedly explaining “what you would do” when you can actually do it via tools.
Use `context7` before implementing against external APIs to confirm signatures/behaviors; capture the takeaway in your notes.

---

## 4. Validate and Record Outcomes

1. Run targeted validations, preferring narrow scope first (e.g., module tests) and broadening as needed (e.g., `uv run pytest`, `uv run ruff check`).
2. Capture results:
   - Pass/fail and any notable errors.
   - If validations fail, stop and focus on fixing the failure before moving on.
   - If implementations tied to the `[VALIDATE]` task are not yet complete, mark the validation as `blocked` and do not execute it.
3. In your response:
   - Summarize what changed (files, key logic).
   - Summarize validation results and confidence level, explicitly calling out which checklist `[VALIDATE]` subtask(s) you satisfied (or why they remain pending).
4. If you ran validations that are part of the initiative’s Validation Gate, update the `Validation Gate` section in the checklist (or plan to do so in the next checklist update) so that it reflects which checks have passed, failed, or are pending.

If you could not run validations, explicitly say so and why.

---

## 5. Update Checklist and Notes

Assuming you have enough information to update the checklist:

1. Modify the checklist file:
   - Mark the executed subtask as `[x]` when appropriate.
   - Add or adjust file paths, tests, and Branch references if they became concrete.
   - If you decomposed a broad task, ensure the new sub-subtasks are added with IDs/prefixes, scoped descriptions, and validation commands; leave unexecuted children open.
   - Update the **Execution Readiness / Implementation Coverage** paragraph if you added or re-linked any `[PLAN]`, `[IMPLEMENT]`, or `[VALIDATE]` tasks so the PLAN→IMPLEMENT→VALIDATE mapping stays accurate.
2. Under **Notes & Learnings**, add a dated entry describing:
   - What you implemented.
   - Any unexpected findings or decisions.
3. If the task remains partially done or blocked:
   - Update its status and note why (e.g., waiting on external command output).
   - Add follow-up subtasks if new work was discovered.

Write only the minimal necessary changes to the checklist file.

---

## 6. Propose the Next Task

Re-read the current checklist in its entirety to understand the current state of the checklist. Review all open items, and determine what should be the single *Recommended next subtask*.

End with a concise sentence naming the single *Recommended next subtask* that should follow, along with a short rationale. Derive this strictly from explicit user instructions or, if none exist, the highest-priority unblocked item in the checklist—no special markers or stored notes are required.

Choose a next task that:

- Respects dependencies.
- Keeps momentum toward the initiative’s goals.
- Maintains a balance between checklist-workflow/research and implementation/validation.

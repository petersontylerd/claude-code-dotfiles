---
description: Modify initiative checklist currently in context with new requirements
---
# `update-checklist`

You are updating the **structure and metadata** of an existing initiative checklist in light of:

- New understanding,
- Scope changes,
- Or feedback from prior reviews or execution steps.

This command focuses on **editing the checklist file itself**, not on making new code changes.
---

## 1. Clarify Update Intent

1. Ask the user:
   - What has changed in understanding or scope?
   - Whether there are specific parts of the checklist they want adjusted (e.g., new Major Task, splitting a Subtask).
2. Restate the requested adjustments in your own words.

Do not proceed until update intent is clear.

---

## 2. Read the Current Checklist

1. Use the checklist path from session context (default: `scratchpaper/initiatives/$INITIATIVE_NAME/checklists/<raw|optimized>/*.md`; only one `.md` is expected per directory); only ask for the path if it is missing or conflicting.
2. Summarize:
   - Existing Major Tasks.
   - Notable Subtasks and their prefixes/tags.
   - Any obvious imbalances (too much `[PLAN]/[RESEARCH]` vs `[IMPLEMENT]/[VALIDATE]`).
   - Whether **Major Task 0** still appears first with the canonical fenced `.sh` block and the user-vs-agent command guidance intact.

If you cannot find the checklist file, ask for its path.

---

## 3. Apply Structural Updates

1. For requested changes (or obvious structural fixes that keep scope consistent with the clarified intent):
   - Add new Major Tasks/Subtasks with appropriate prefixes and tags, following the canonical ID and status schema:
     - Major Tasks numbered (`1`, `2`, `3`, …).
     - Subtasks with IDs like `N.A`, `N.B`, and when split, `N.A.1`, `N.A.2`, etc.
     - Represent tasks as markdown checklist items (`[ ]` for open/todo, `[x]` for done, optional `[~]` for in-progress), with inline `blocked` annotations when applicable.
   - Split complex items into smaller, well-scoped subtasks (use IDs like `2.C.1`, `2.C.2`).
   - Reorder tasks to reflect new priorities and dependencies.
   - Enforce ordering within each Major Task as `[PLAN]/[RESEARCH]` → `[IMPLEMENT]` → `[VALIDATE]`; treat any `[VALIDATE]` that precedes its referenced `[IMPLEMENT]` as blocked until reordered after the implementation.
   - If you believe new scope needs to be introduced beyond what the user just clarified, pause and confirm that addition before editing the checklist.
2. Maintain existing IDs and prefixes where possible:
   - Update descriptions and tags rather than renaming IDs.
3. Enforce pairing:
   - For any new `[PLAN]/[RESEARCH]` items you add, also add paired `[IMPLEMENT]/[VALIDATE]` items.
   - Ensure existing `[PLAN]/[RESEARCH]` entries continue to reference downstream `[IMPLEMENT]` items and that every `[IMPLEMENT]` references at least one `[VALIDATE]`. Update references if you split/merge tasks.
4. Preserve Major Task 0:
   - Keep it as the first Major Task with its blocking status.
   
Write back minimal edits using the appropirate tools, preserving the ABOUTME header and section headings.
Use `serena` to gather precise file/symbol references when enriching metadata. If new items depend on external APIs, consider a quick `context7` lookup and note key findings.
When editing, stay within the repo; prefer `apply_patch` or `serena` edits, and only create/overwrite files intentionally.
For discovery before edits, use scoped shell tools (`rg --files`, `ls`, `find`, `rg pattern path`) limited to relevant paths.

---

## 4. Strengthen References and Metadata

1. Add or correct:
   - File paths.
   - Symbols or endpoints.
   - Branch references.
   - Ordering of `[VALIDATE]` items so they appear after all referenced `[IMPLEMENT]` tasks.
2. Refresh the **Execution Readiness / Implementation Coverage** note so it reflects the current PLAN→IMPLEMENT→VALIDATE mappings (including any shared validations) after your edits.
3. Ensure the **Validation Gate** and **Definition of Done** sections still accurately describe how the initiative will be validated, and update individual `[VALIDATE]` subtasks (and their references) accordingly if the validation strategy changed.

---

## 5. Log the Update

Under Notes & Learnings:

- Add a dated entry summarizing:
  - What structural changes were made.
  - Why those changes were needed (e.g., scope expansion, risk mitigation).

End with a short summary of the updated checklist shape and any recommended next execution tasks.

---
description: Clean up scratchpaper references created during development.
---
# `/scratchpad-review-and-cleanup`

You are performing a **scratchpad hygiene pass** for an initiative or project.

Your goals:

- Discover relevant scratchpad files.
- Classify each as “promote”, “keep”, or “delete”.
- Propose non-destructive commands for the user to run.

You do **not** directly delete or move files; you only propose commands.

---

## 1. Discover Scratchpad Artifacts

1. Default to `scratchpaper/` and any scratch locations already known from session context; ask the user for additional directories only if needed.
2. List files under:
   - `scratchpaper/initiatives/*/checklists/`
   - Any other `scratchpaper/*` subdirectories relevant to the initiative.
3. Group discovered artifacts by:
   - Checklists vs notes vs experimental code/tests.

If the user indicates additional scratch locations, include those as well.
`serena` is only needed if you must inspect code before recommending promotion. `context7` is generally unnecessary here.
When listing, prefer `list_directory_with_sizes` or `directory_tree` for scoped visibility and keep within `list_allowed_directories`.

---

## 2. Classify Artifacts

For each scratch file, classify it into one of:

- **Promote** — Contains decisions, designs, or examples that should become:
  - Permanent docs (e.g., under `.claude/docs` or `docs/`).
  - Product-plan content (e.g., updated initiative/feature YAML).
  - Inline comments or test cases in code.
- **Keep as scratch** — Still actively useful as a working surface.
- **Delete** — Temporary experiments or obsolete notes with no ongoing value.

Explain the reasoning for each classification briefly.

---

## 3. Propose Commands (No Direct Deletion)

For each artifact:

- If **Promote**:
  - Suggest specific moves or copies (e.g., `mv scratchpaper/notes/x.md docs/initiatives/x.md`).
  - Specify any follow-up edits needed in planning artifacts or docs.
- If **Keep as scratch**:
  - No file system changes required; optionally suggest renaming for clarity.
- If **Delete**:
  - Propose `rm` commands, but **do not run them**.

Group commands in your response under a clear heading, e.g., “Commands for you to run (optional)”.

---

## 4. Update Notes & Checklist

If a checklist is associated with this initiative:

1. Add a Notes & Learnings entry indicating:
   - That a scratchpad review was performed.
   - Which files were promoted, kept, or slated for deletion.
2. If needed, add subtasks:
   - `[DOC]` items to promote scratch content to permanent artifacts.
   - `[IMPLEMENT]` items to incorporate scratch code into the main codebase.

Make minimal, clear edits to the checklist file to reflect this work.

---

## 5. Final Summary

End with a concise summary:

- Count of files per classification (Promote/Keep/Delete).
- Any especially important artifacts that were promoted.
- Any follow-up tasks you recommend adding to the checklist.

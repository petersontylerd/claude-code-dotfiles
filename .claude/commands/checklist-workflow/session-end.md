---
description: Close development session by updating checklist with current session state
---
# `/session-end`

You are closing out a **coding session** for an initiative/feature.

Your goals:

- Summarize what happened this session.
- Update the checklist with outcomes and new insights.
- Record a clear pointer for where to resume next time.

Do not begin new tasks in this command; focus on documenting what happened and setting up the next session.

---

## 1. Session Summary

1. Review:
   - The checklist file (path from session context; only ask if missing).
   - Any tasks executed during this session (from conversation context).
2. Summarize:
   - Tasks completed.
   - Tasks partially completed or blocked.
   - Any unexpected findings or issues.

Keep this summary focused on concrete work and outcomes.

---

## 2. Update the Checklist

1. Mark completed tasks `[x]` and update statuses for partially done items.
2. Reopen or mark `blocked` any `[VALIDATE]` items whose referenced `[IMPLEMENT]` tasks are not complete, and reorder so `[VALIDATE]` entries stay after their implementations.
3. If you identify any critical Subtasks that should be included on the checklist but are missing, propose the Subtask(s) and specify the related Major Task, Subtask text, and Subtask purpose. Verify your proposal with the user before making any additions.
4. Strengthen references:
   - Add file paths, commits, and test references where relevant.
   - Keep branch references aligned with the session’s active branch; do not re-prompt unless context conflicts.
5. Refresh the **Execution Readiness / Implementation Coverage** section so that every `[PLAN]/[RESEARCH]` still cites downstream `[IMPLEMENT]` IDs, every `[IMPLEMENT]` cites its `[VALIDATE]` IDs, and shared validations are called out explicitly.
6. Update the **Validation Gate** entries to reflect validations run (pass/fail/pending) during this session, keeping them aligned with the `[VALIDATE]` subtasks they correspond to.

Use the appropriate tools to apply small, careful edits.
If new follow-ups rely on external APIs, optionally use `context7` to confirm details and note them in Notes & Learnings.
Keep checklist edits within `list_allowed_directories`; prefer `edit_file` (with `dryRun` if uncertain) for updates.
For discovery of checklist location or related scratch files, use `list_directory`/`list_directory_with_sizes`/`directory_tree` scoped to allowed paths.

---

## 3. Notes & Learnings

Under **Notes & Learnings**, add a dated entry capturing:

- What was achieved this session.
- Key decisions made.
- Any risks or open questions discovered.

If there were failures (tests, commands, etc.), explicitly note them with short context.

---

## 4. Resume Instructions

1. Identify the **single highest-leverage next task** to tackle in the next session (prefer explicit user instructions; otherwise use the highest-priority unblocked checklist item).
2. Mention this next task explicitly in your response with a brief rationale so the next `session-start` can pick it up immediately. Do not add special “NEXT_SESSION_FOCUS” fields to the checklist; rely on the checklist ordering, statuses, and notes you already maintain.

This ensures that a future agent (or you) can restart efficiently without rereading the entire history while keeping the checklist free of extra markers.

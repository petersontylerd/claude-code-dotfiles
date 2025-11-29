---
description: Improve the prompt for a single INITIATIVE_NAME by loading the raw prompt and saving the optimized prompt to that initiative’s optimized directory
argument-hint: INITIATIVE_NAME=<initiative_name>
---

You are an AI assistant whose job is to rewrite a draft prompt so it works optimally in a two-stage workflow:

1. A prompt is used to generate an initiative plan using `./.claude/commands/checklist-workflow/create-initiative-plan.md`.
2. That initiative plan is then transformed into a detailed, executable checklist using `./.claude/commands/checklist-workflow/plan-to-checklist.md`.

## Quick Checklist — DO NOT SKIP ANY STEP

1. **Review AGENTS.md** - Located at `./AGENTS.md`
2. **Review downstream prompts**: Review both `create-initiative-plan.md` and `plan-to-checklist.md` so you know what kind of input each prompt expects and the purpose of each prompt. Use that understanding to shape the improved version of the draft prompt, but do **not** reference those downstream prompts directly in the improved prompt text.
3. **Read and rewrite the draft prompt** (loaded from `./scratchpaper/initiatives/$INITIATIVE_NAME/prompts/raw/*.md`, exactly one `.md` is expected in that directory) following the objectives below (preserve scope, add structure, avoid downstream references).
4. **Save the improved prompt** as a `.md` file to `./scratchpaper/initiatives/$INITIATIVE_NAME/prompts/optimized/`. For filename pattern, use `<YYYY-MM-DD>-<initiative-or-feature-name>-checklist.md`.
5. **Verify and report**: Confirm the new .md file exists in `./scratchpaper/initiatives/$INITIATIVE_NAME/prompts/optimized/` and reply only with `✅ Saved optimized prompt to ./scratchpaper/initiatives/$INITIATIVE_NAME/prompts/optimized/`—do **not** print the prompt contents.

⚠️ Skipping any checklist step or printing the improved prompt text is a task failure.

### Your objectives

Given the draft prompt located at `./scratchpaper/initiatives/$INITIATIVE_NAME/prompts/raw/*.md`:

1. **Preserve intent**

   * Keep the original goal and scope of the initiative intact.
   * Retain any domain-specific requirements or non-negotiable constraints.

2. **Increase clarity and completeness**

   * Resolve vague language and remove ambiguities.
   * Remove redundancy and irrelevant details.
   * Make implicit assumptions explicit when helpful for planning.
   * Highlight key constraints (timeline, resources, tools, dependencies, risks).
   * Enhance user's prompt with additional context, domain knowledge, and requirements where it will be additive to the user's goal. However, do not load the prompt with additional fluff and bloat that may produce a prompt that deviates from the user's goal. Only add content when you are 100% confident your additional input will be additive.

3. **Avoid internal implementation details**

   * Do **not** mention how the output will be post-processed.
   * Do **not** mention file paths, repositories, or internal tools that were not part of the initially provided draft prompt.
   * But *do* preserve file paths, repositories, and internal tools that were included in the initially provided draft prompt.
   * Do **not** say that you are “improving” or “rewriting” a prompt.
   * The improved prompt should read as a standalone prompt that a user could give directly to a planning model.

### Output requirements

* Return **only** the final, improved prompt text that should replace the draft prompt.
* Do not include commentary, explanations, or meta-notes about what you changed.
* The improved prompt may use markdown formatting (headings, lists) if it helps structure the response.

### Workflow Order (DO NOT DEVIATE)

1. Review `create-initiative-plan.md` and `plan-to-checklist.md`.
2. Load the draft prompt from `./scratchpaper/initiatives/$INITIATIVE_NAME/prompts/raw/*.md` and rewrite it according to the objectives below.
3. **REQUIRED DELIVERABLE** = A `.md` file saved to `./scratchpaper/initiatives/$INITIATIVE_NAME/prompts/optimized/` (filename pattern `<YYYY-MM-DD>-<initiative-or-feature-name>-checklist.md`).
4. Verify the file exists.
---
description: Provide a second opinion on the optimized prompt for a single INITIATIVE_NAME
argument-hint: INITIATIVE_NAME=<initiative_name>
---

You are an expert lead software engineer reviewing the work of a junior software engineer. Ground your review in this repository’s architecture, conventions, tests, and docs: identify where the artifact aligns or conflicts with existing patterns/modules/data contracts, what should be reused, and where gaps create risk. For every conflict or gap you flag, pair it with a concrete, repo-aligned remediation (reuse, refactor, relocate, add coverage). Highlight downstream impacts (maintainability, test coverage, integration points). Maintain the required structure, rules, and intent of this prompt while integrating your repository-informed judgment.

You are evaluating how effectively the junior engineer produced an `optimized prompt` from a `raw prompt`, using a given `instruction set`.

You will review the following artifacts:

- **Raw prompt** initially provided for refinement: read from the file at `./scratchpaper/initiatives/$INITIATIVE_NAME/prompts/raw/*.md` (only one `.md` is expected in this directory)
- **Instruction set** that the junior engineer was asked to follow:
  `./.claude/commands/agent-doublecheck/improve-prompt.md`
- **Optimized prompt** produced by the junior engineer: read from the file at `./scratchpaper/initiatives/$INITIATIVE_NAME/prompts/optimized/*.md` (only one `.md` is expected in this directory)

Your assessment **must** include:

1. **Strengths**
   - Identify specific strengths in the optimized prompt.
   - Call out concrete examples where the junior engineer followed the instruction set well or improved the raw prompt in meaningful ways.

2. **Weaknesses & Remediations**
   - Only raise weaknesses when they represent critical gaps or material risks to clarity, fidelity, or usability.
   - For each weakness, propose a clear remediation:
     - Explain *why* it is a weakness.
     - Provide a concrete suggestion or example of how to fix it (e.g., revised wording, added constraints, improved structure).
   - Do not advance the initiative until each critical weakness is either applied or explicitly waived with rationale; if waived, record the waiver so downstream steps know the optimized prompt is accepted as-is.

3. **Deviations from the Instruction Set**
   - Only flag deviations that constitute critical gaps or material misalignments with the instruction set when transforming the `raw prompt` into the `optimized prompt`.
   - Treat these as critical issues.
   - For each deviation:
     - Describe the deviation precisely.
     - Explain the impact (e.g., lost constraints, weaker guidance, increased ambiguity).
     - Propose a specific remediation, including example revisions to bring the optimized prompt back into alignment with the instruction set.

4. **Overall Evaluation**
   - Provide a brief overall evaluation of the optimized prompt’s quality, clarity, and faithfulness to:
     - The original intent of the raw prompt.
     - The requirements in the instruction set.

**Output format:**

Structure your response using clear sections with headings, for example:

- `Summary`
- `Strengths`
- `Weaknesses and Remediations`
- `Deviations from the Instruction Set (Critical) and Remediations`
- `Overall Evaluation`

Within each section, use bullet points or numbered lists for readability and concision.

At the end of your assessment, provide an outline of your recommended changes and then explicitly ask the user:

> “Would you like me to apply these remediations directly to the file at \`./scratchpaper/initiatives/$INITIATIVE_NAME/prompts/optimized/*.md\`?”

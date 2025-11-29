You are a coding assistant working from the complete validation results: `$RESULTS`.

1. **Analyze failures**

   * Comprehensively review all errors, failures, and warnings.
   * Identify the specific code locations and implementations responsible for each issue.

2. **Plan minimal fixes**

   * For each failure, design the smallest-scope code change that will make the test or evaluation pass.
   * Prefer localized changes over broad refactors unless absolutely necessary.

3. **Implement and re-run**

   * Apply the planned code changes.
   * Re-run only the **relevant** tests and evaluations needed to verify the fixes.
   * Repeat this modify → re-run cycle until all affected tests and evaluations pass.

4. **Test modification policy**

   * You **must not** modify tests or evaluation code unless there is a clear flaw.
   * If you believe a test or evaluation is incorrect or must be updated:

     * **Stop immediately.**
     * Explain why you think it is flawed.
     * Wait for my explicit approval before proposing or making any test/evaluation change.

5. **When you cannot run commands**

   * If you cannot run `pytest`, `ruff`, or other commands yourself due to permission issues or network access barriers:

     * Provide me with the **exact commands** to run in another terminal.
     * Limit the commands to what is necessary to re-test or re-evaluate the changed functionality.
     * Make them broad enough to cover all tests/evaluations that need re-checking, but **do not** ask me to re-run the entire test suite or full TDD cycle unnecessarily.

6. **Final report**

   * When all tests and evaluations pass, produce a concise summary including:

     * Which files/functions you changed.
     * The root cause of each failing test or evaluation.
     * How your change resolves the issue and why the test/evaluation now passes.

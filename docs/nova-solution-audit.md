# Nova "Green-SLA" Shipping Copilot – Solution Audit and Framing

## Problem Context: Failing CI/CD Drains Velocity

Modern software teams often struggle with red builds, flaky tests, and broken pipelines that halt progress. A failing CI job means engineers spend hours babysitting pipelines – parsing logs, rerunning tests, and applying manual fixes. Current CI systems largely serve an alert-and-block role: they run tests and notify you of failures, but don't help fix the underlying issues. As a result, shipping velocity suffers; merges are delayed and developers lose focus context-switching to debug CI problems.

Why Nova? The gap is clear – while editors have coding copilots to assist with writing code, there's no "shipping copilot" ensuring that code actually gets to production. This is the problem Nova addresses: automatically turning failing pull requests into passing ones (or providing a bounded plan) so that every PR arrives shippable with minimal human intervention.

## Solution Overview: Nova as a Self-Healing CI/CD Copilot

Nova is proposed as an autonomous CI/CD autopatcher – essentially a "self-healing" layer for your pipeline. On each pull request (PR), Nova will automatically:

1. Reproduce the failure in a hermetic environment (same dependencies, seeds, etc.),
2. Diagnose the root cause,
3. Plan a fix within strict safety limits,
4. Apply a minimal patch on a side branch, and
5. Re-run the tests to verify the fix.

It repeats this loop until the PR's checks go green or it reaches a defined attempt limit. If it cannot fix the issue, Nova will post a detailed analysis and plan for a human to review. All of this happens as part of your CI flow, so by the time a developer looks at the PR, it's either already green or comes with a clear path to green.

In short, Nova acts as a "shipping copilot": instead of just telling you something's wrong, it actively makes failing checks pass – safely and automatically. This turns the traditional CI promise into a "Green-SLA": an expectation that builds stay green by default, with Nova doing everything possible to meet that standard.

## Mapping the Runbook to Nova's Features

Teams often have a runbook for CI failures – a series of manual steps engineers follow when a build breaks. Nova codifies that entire process into product features, creating a closed-loop, alert-first automation. For example:

- **"Stop the line"** (halt merges, notify team) – Nova implements this via incident state + alerts (Slack notifications, GitHub check failures). If the main branch is broken, Nova posts status updates and prevents further merges.

- **Reproduce in the same environment** – Nova uses a hermetic test runner (consistent base images, pinned dependencies, fixed random seeds) to ensure it sees the exact same failure as CI.

- **Focus on first error** – Nova includes a log parser that extracts the first failure or error signature, so it concentrates on the root cause rather than getting lost in cascading errors.

- **Time-box the investigation, then revert** – Nova has an auto-revert policy: if it can't fix the build within a grace period or a couple of attempts, it can automatically roll back the offending commit (this is configurable and initially off until you're comfortable).

- **Bisect when cause is unclear** – Nova provides an on-demand bisect job to pinpoint which commit introduced a failure. This isn't run every time, but you can trigger it (or even automate it) if a failure's cause isn't obvious.

- **Detect flakiness and quarantine** – Nova includes a flake classifier that watches for tests that fail intermittently. It can label or quarantine flaky tests (e.g., move them out of required checks) so they don't keep spurious failures from blocking merges.

- **Apply the smallest safe fix** – Nova's Green-SLA autopatcher tries to make the minimal change necessary (bounded by N attempts, F files, L lines of code) to resolve the failure. The focus is on small, surgical fixes that are easy to review.

- **Explain every change** – Every Nova-generated patch comes with an explanation (a one-paragraph rationale) and links to relevant logs or artifacts. This way, developers can understand why the change was made.

- **Enforce guardrails** – Nova uses policy-as-code (OPA/Rego) plus scanners to enforce rules (e.g. no touching certain sensitive files, respecting CODEOWNERS, limiting how much can change). These guardrails ensure Nova's fixes stay within agreed boundaries.

By mapping the manual runbook steps to these capabilities, Nova ensures that the entire CI failure-handling process is owned end-to-end by automation. What used to be a page of instructions in a Wiki is now baked into the CI/CD pipeline itself.

## Key Components and Configuration

Nova's solution is delivered through a combination of config-as-code, CI pipeline hooks, and lightweight CLI tools/scripts. The major components include:

### Nova Configuration (nova.yml)

A file (e.g. `.github/nova.yml`) in the repo defines Nova's operating limits and policies. For example, you can set limits like `max_attempts: 2` (Nova will try at most 2 patches), `max_files_changed: 5`, `max_loc_delta: 40` (no patch bigger than 40 lines added/removed) etc. It also defines risk categories – e.g., Nova might auto-commit safe fixes (linting, formatting, simple type errors) but only suggest changes for higher-risk issues (dependency upgrades, major refactors).

The config also lists alert channels and rules (Slack, GitHub comments, PagerDuty escalation) and policy settings (like which paths are protected, whether to enforce CODEOWNERS checks, etc.). All these settings make Nova's behavior transparent and tunable via versioned code.

### GitHub Actions Workflows

Nova integrates into CI via standard workflows. The solution provides ready-to-use YAML workflows:

**PR Auto-Fix Workflow** (e.g., `.github/workflows/nova-ci-rescue.yml`): This runs on every pull request update. It checks out the code, ensures the environment is ready (using a preflight script), then invokes Nova's CLI (for example: `nova run --pr $PR_NUMBER --ci "pytest -q"`). Nova then attempts to fix any test failures on that PR. If Nova makes changes, it commits them to a new branch (like `nova/fix/123` for PR #123) and pushes, so the PR picks up the changes.

**Main Branch Guardian Workflow** (`nova-main-guardian.yml`): This runs on pushes to the main branch (or whatever the "protected" branch is). It executes the test suite in a controlled way (capturing the first error to a log). If the suite fails, this workflow will handle incident response: it can create a GitHub Check run that shows the failure, post a Slack alert to notify the team that the main branch is broken, and optionally trigger a PagerDuty escalation if no one responds in a given time.

**On-Demand Bisect Workflow** (`nova-bisect.yml`): This is a manually-triggered (`workflow_dispatch`) job that takes inputs (a "good" last-known-green SHA, a "bad" current SHA, and a test command). It uses `git bisect` under the hood to automatically run the failing test on different commits to pinpoint which commit introduced a failure.

### Utility Scripts

Alongside the workflows, Nova provides scripts to assist in the CI environment:

- `scripts/ci/preflight.sh` – This runs before Nova's main logic. It checks that the environment is sane and sets consistent environment settings.
- `scripts/ci/first_error.sh` – Given a full CI log, this script finds the first occurrence of a failure and prints that section.
- `scripts/ci/env_fingerprint.sh` – This gathers information about the environment and dependencies and writes it to an artifact file.

### Guardrail Policies (OPA/Rego)

The solution includes a policy file `policy/guardrails.rego` which encodes organization-specific rules for patches. Nova's orchestrator can query this policy before applying any fix. For example, the policy might say:

- "If more than 5 files are changed or more than 40 lines are added/removed, that's a violation (too large of a fix)."
- "If the diff touches any file in `migrations/` or `secrets/` or other sensitive directories, that's a violation."
- "If multiple distinct areas are changed in one patch, flag it."

If any such rule is violated, Nova will not auto-commit the patch; instead, it can either skip that fix or mark it for human review.

### Alerts and Notifications

Nova is designed to integrate with team communication channels:

**Slack**: You can configure a Slack webhook in the Nova config. The solution provides a sample shell script (`alerts/slack_payload.sh`) that formats a message with an emoji/status and a direct link to the relevant CI run or PR, then POSTs it to Slack.

**PagerDuty (PD)**: For critical pipelines (like prod deploys), Nova can escalate to PagerDuty after a certain time. The config's alert rules allow an `escalate_after_minutes: X` setting.

**GitHub Checks and PR comments**: Nova leverages GitHub's status checks API. For instance, the "Nova CI Rescue" workflow can create a check run that reports the status of Nova's attempts. If Nova fails to fix a PR, it can mark the check as "action required" and attach logs or the plan for fixing.

All these components work together: the workflows trigger Nova at the right times, the config and policies constrain its behavior, and the scripts plus integration hooks let Nova communicate what it's doing.

## Autopatch Loop Mechanism: "Plan → Patch → Verify"

At the heart of Nova is an autopatch loop that embodies the "reproduce and repair" cycle:

1. **Reproduce & Capture**: Nova starts by running the test suite (or specific failing checks) in an isolated environment to see the failure firsthand. It captures the logs, and using the `first_error.sh` logic, identifies the first point of failure.

2. **Plan**: Based on the failure classification and Nova's internal knowledge base, it formulates a repair plan. The plan is essentially: "What minimal change could fix this?" Nova always stays within the risk budget defined – e.g., "At most 2 attempts for this PR, touching no more than 5 files and adding/removing ≤ 40 lines total."

3. **Generate Patch**: Nova then uses AI (and possibly some templated fixes for known issues) to generate the code changes according to the plan. This could involve editing a few lines in a function, adding a small test, updating a version in a config file, etc. The emphasis is on minimality – the smallest possible diff that could resolve the failure.

4. **Apply to Side Branch**: Nova never commits directly to main. It commits the patch to a separate branch (e.g., `nova/fix/<PR-number>` or a similarly prefixed branch). This approach means that the original PR branch isn't altered by Nova – instead, the PR is updated via a new commit from Nova on a side branch.

5. **Run Tests on the Patch**: After applying the patch, Nova triggers the CI checks again. Now we see if the fix worked. If all tests pass, wonderful – Nova has managed to turn the PR green. If there's still a failure (or a new failure), Nova records that outcome for the next iteration.

6. **Critique & Iterate**: If the tests are still failing, Nova goes back to step 1 or 2: it analyzes the new failure and will then come up with a refined plan or a new plan for the new error. Nova will iterate this cycle, but only up to a fixed number of attempts (`max_attempts`) to avoid an infinite loop.

7. **Decide & Report**: After either succeeding or exhausting attempts, Nova makes a decision:

   - **Success**: Nova will update the PR with the fix branch commit(s) and typically add a comment like "✅ Nova auto-fix applied: all checks are now passing."
   - **Failure/Exceeded Budget**: If Nova couldn't fix the issue within the set attempts, Nova will comment with a failure report and attach artifacts.

8. **Explain**: A key part of Nova's philosophy is explainability. Each Nova-generated patch comes with a one-paragraph rationale explaining why the change was made and evidence that it's safe.

Throughout this loop, Nova is constrained by guardrails and policy at every step. It won't, for example, decide to pull in a new library or make a database schema change as a fix – those are beyond its scope unless explicitly allowed.

## Safety and Guardrails

Nova's design prioritizes safety and control, recognizing that teams need to trust it gradually. Key safety mechanisms include:

- **No direct commits to main**: All fixes go to a `nova/fix/...` branch, keeping the primary branch untouched.
- **Strict change budgets**: Nova enforces quantitative limits on its fixes (max files/LOC changed, max attempts).
- **Protected areas**: Certain files or directories can be declared off-limits or sensitive.
- **CODEOWNERS enforcement**: Nova can be set to respect your repo's CODEOWNERS rules.
- **Policy-driven guardrails**: The OPA/Rego policy file encodes rules in a single source of truth.
- **Risk-tiered actions**: Not all fixes are equal. Nova categorizes fixes by risk (low/medium/high-risk).
- **Human oversight for exceptions**: If Nova hits a guardrail, it will defer to humans.

## Incident Handling and Alerting

Nova treats CI failures as first-class incidents that need both attention and action:

**Main branch failures**: When a commit to main causes a red build, Nova's Main Guardian comes into play. It will immediately surface the issue via multiple channels and can automatically pause any merge queues or deployment pipelines.

**Pull request failures**: When a PR's CI is failing, Nova's PR Auto-Fix workflow will try to fix it. While doing so, it can post status updates and notify on Slack as well.

**Alert tuning**: Not every failed test needs a loud alert. The Nova config allows tuning what conditions trigger which alerts.

## On-Demand Tools: Bisect and Flake Management

Two special cases in CI failures are when the cause is unknown and when the cause is intermittent (flaky tests). Nova includes tools for both:

**Automated Bisect**: Nova has a workflow to automate `git bisect`. If you supply a range and a command that determines "good vs bad", Nova will binary-search through your commit history to find exactly which commit introduced the failure.

**Flake Detection & Quarantine**: Nova's orchestrator can identify patterns where a test fails but on re-run passes. For known flaky tests, Nova can automatically quarantine them.

## Adoption Path and Rollout Stages

Introducing an autonomous tool into CI/CD should be done carefully. Nova's solution is designed to be adoptable in stages:

- **M0 – Explain-Only Mode**: Start with Nova not making any changes at all. Nova will analyze failures but only output explanations and possible solutions.
- **M1 – Automatic Small Fixes**: Allow Nova to auto-fix very low-risk issues like lint errors and simple test assertions.
- **M2 – Moderate Fixes & Multi-File Changes**: Nova tackles more complex issues within a contained scope.
- **M3 – Flake & Stability Management**: Nova becomes proactive about the health of the test suite itself.
- **M4 – Deploy Guardian**: Nova's self-healing extends into the deployment phase.

## Value Proposition and Differentiation

Nova is positioned not as a traditional CI tool or a generic coding assistant, but as a new kind of outcome-focused CI companion:

- **Core Promise (Green-SLA)**: Nova aims for "green by default" CI – it will do everything possible (within safe limits) to get a failing build back to green.
- **Outcome-Focused vs Tool-Focused**: Unlike traditional CI/CD tools that stop at running tests and reporting failures, Nova actually acts to resolve those failures.
- **Minimal & Safe Fixes**: Nova's fixes are intentionally small and auditable. Each patch is constrained in size and comes with an explanation and evidence.
- **Safety & Control**: A huge part of Nova's differentiation is the safety layer with policies, config, and human approvals built-in.

## Operational Details and Evidence

The described GitHub Actions workflows and scripts are straightforward to implement. They follow best practices and give Nova the needed permissions to push fix branches and update PRs. The use of hermetic test runs, first error focus, minimal patch strategy, and guardrails via Rego all show technical soundness.

The solution appears technically feasible and robust, covering the full spectrum from detection to fix to notification. Each piece is built on proven practices, which increases the likelihood that Nova can be adopted without a huge learning curve.

## Product Framing and Language

In positioning Nova, it's important to convey that this is not just another CI tool, but a new category of developer assistant focused on shipping quality code faster:

- **Category Name**: Self-Healing CI/CD
- **Role**: Shipping Copilot
- **Core Promise**: Green-SLA
- **Unit of Value**: "Minutes to Green" and "% PRs Auto-Fixed"
- **Patch Style**: "minimal, auditable diffs"
- **Risk Layer**: "policy-driven guardrails"

## Conclusion

The Nova "Green-SLA Shipping Copilot" solution provides a comprehensive answer to the problem of failing CI pipelines by automating the diagnosis and repair process with safety and accountability. The audit shows that it covers all the critical bases: effectiveness, safety, transparency, completeness, adaptability, and vision.

If implemented and calibrated correctly, Nova could significantly improve engineering productivity and confidence in the CI/CD process. It represents a promising step towards truly self-healing pipelines that change the mindset from "oh no, the build is red, who's going to fix it?" to "the build is red, but Nova is on it – it might be green by the time I get back from lunch."

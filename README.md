Nova: Self-Healing CI/CD

Actions/GitLab/Buildkite run your checks; Nova makes them pass — safely, automatically.

Nova is an autonomous CI/CD autopatcher. On every pull request, Nova reproduces failures, maps them to likely fixes, proposes a minimal diff, commits the fix on a safe side-branch, and re-runs your pipeline until the suite is green. The result: every PR arrives shippable (automatically!), backed by full auditability and guardrails. In short, Nova isn't just another coding assistant – it's a shipping copilot for your code delivery pipeline.

Why Nova? (The Core Problem)

Modern code editors have coding copilots (e.g. GitHub Copilot, Cursor, Claude Code) to help write code, but shipping that code safely to production is still fraught with friction. CI/CD is often where development velocity dies: broken builds, flaky tests, blocked merges, and constant babysitting of pipelines. Existing CI/CD tools mostly alert you to failures and block merges, but none reliably act to repair the problems.

This gap creates massive waste. Writing software is easy; shipping it safely, at velocity, is hard. Every engineering org spends countless hours fixing red builds, re-running flaky tests, and diagnosing broken deployments – a trillion-dollar productivity problem industry-wide. Nova closes this loop by not only detecting CI failures, but automatically fixing them. (As we like to say: "Alerts are cheap; fixes are priceless. Nova does both.")

How Nova Works (Autopatch Loop)

Nova operates an intelligent four-step loop whenever it encounters a failed build or test, continually iterating until the pipeline goes green (or a safe limit is reached):

Plan – Classify the failure and draft a repair plan within a risk budget (deciding what kind of fix is safe to attempt).

Generate – Propose a minimal patch to address the issue (no more than ~40 lines changed, applied on a side branch).

Patch – Apply the changes on a new branch (e.g. nova/fix/...), never touching the main branch directly.

Critic – Re-run the CI checks on the patched branch. If failures persist, Nova critiques the result and goes back to planning the next fix, iterating until the build is green or a sensible attempt limit is reached.

Each Nova-generated patch comes with a one-paragraph rationale explaining the change, diff stats, and provenance info for audit. All fixes are done under strict guardrails – Nova only commits to a separate fix branch and within the predefined safety limits – ensuring you remain in control of your codebase.

Features & Current Capabilities (v1: PR Auto-Fix)

Nova's initial focus is automatic pull request repair. On every new or updated PR, Nova can analyze the CI results and:

Summarize the failing checks and potential root causes (so you understand what went wrong).

Automatically apply fixes for common failure causes (on a nova/fix branch) and re-run the pipeline to verify the solution.

Handle even PRs with minimal or no test coverage by targeting issues like lint errors, type errors, import problems, build failures, etc., and even generating basic smoke tests on the fly to cover critical paths if needed.

This essentially provides a "green build SLA" for your pull requests – Nova works behind the scenes to ensure your PRs end up green and merge-ready with little to no human intervention. It's not magic; it's systematic autopatching of the mundane breakages that slow teams down.

Metrics Nova Improves: Nova is measured by how much it boosts your CI/CD efficiency. Key metrics include:

Time-to-Green: ↓ Decreased – Faster turnaround to get failing pipelines back to green.

Red PR Auto-Fix Rate: ↑ Increased – A higher percentage of broken PRs are automatically fixed without developer input.

Accepted Diff Rate: ↑ Increased – Most of Nova's proposed patches are minimal and accurate, so maintainers accept them at a high rate.

Reviewer Babysitting Time: ↓ Reduced – Less time spent by developers manually troubleshooting CI issues and babysitting pipelines.

Roadmap: From PR Patches to Full Autopilot

Nova's vision is self-healing CI/CD. We're starting with the most pressing pain point (PR fixes) and expanding towards an autonomous CI/CD guardian. Planned stages:

V1 (Current) – PR Auto-Fix: Focus on minimal diffs to fix linting errors, type failures, simple test failures, import/build issues, etc., on pull requests. (This is the current "wedge" feature proving out Nova's value.)

V2 – Policy & Test Synthesis: Enforce org-specific policies and standards (conventions, security checks, etc.) and automatically generate missing micro-tests to improve coverage. Nova will not just fix breaks, but also proactively add tests or adjustments to meet compliance/coverage requirements.

V3 – Flake & Reliability Stabilizer: Identify flaky tests or unreliable infrastructure in CI. Nova will quarantine or rewrite flaky tests and optimize CI execution (for example, intelligent test selection or parallelization tweaks) to improve reliability and speed.

V4 – Deploy Guardian: Extend Nova's self-healing to deployments. Monitor canary releases and SLOs; if a release is failing or degrading, Nova can auto-rollback or auto-forward to a safe state and even prepare surgical PRs to address the root cause of production issues.

Endgame: Nova becomes the neutral autopilot brain for any CI/CD system, guaranteeing that every code change from PR to production stays green. In the endgame, you can trust that if a pipeline turns red, Nova will handle it or guide you to the fix – ensuring every PR is shippable, automatically.

Getting Started

You can integrate Nova into your existing CI pipeline in minutes. For example, on GitHub Actions you can add a workflow file to trigger Nova on pull requests:

# .github/workflows/nova.yml
name: Nova CI Rescue
on:
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  nova:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      actions: read
      checks: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: 
          python-version: "3.12"
      - run: pip install nova-ci-rescue
      - run: nova run --pr "${{ github.event.pull_request.number }}" --ci "pytest -q"
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}


In the above workflow, Nova is installed via pip and then invoked on the current pull request. The --ci "pytest -q" argument tells Nova how to run your test suite (in this case, using pytest; you can replace this with your build/test command). Note: Nova uses OpenAI's API under the hood for code reasoning and generation – be sure to provide your API key as an environment variable (OPENAI_API_KEY) or secret in your CI setup.

Nova can run on other CI platforms (GitLab CI, Buildkite, etc.) in a similar way: install the nova-ci-rescue package in your pipeline and execute nova run pointing to the current PR or commit and your test command. Wherever your tests run, Nova can step in to make them pass!

Configuration

Nova's behavior can be tuned via a configuration file (by default, .github/nova.yml in your repo). Here is an example configuration and what it means:

limits:
  max_attempts: 3
  max_files_changed: 5
  max_loc_delta: 40
risk:
  auto_commit: ["lint", "format", "import", "type"]
  suggest_only: ["dependency", "schema"]
features:
  generate_smoke_tests: true
  test_impact_selection: true


limits: Safety limits to control Nova's scope. In the above example, Nova will try at most 3 attempts to fix a PR, will not modify more than 5 files, and will keep the total lines of code changed under 40. These limits ensure fixes remain minimal and reviewable.

risk: Categories of fixes and how to handle them. Here, certain low-risk fix types (lint, format, import, type errors) are allowed to be auto-committed by Nova, whereas riskier changes like dependency upgrades or schema migrations are marked as "suggest_only" (Nova will propose a fix but not commit it automatically, prompting a human to review/approve). This risk budget mechanism keeps Nova's automated changes safe.

features: Optional feature toggles. generate_smoke_tests: true allows Nova to create simple smoke tests for uncovered code paths when tests are lacking, helping to prevent regressions. test_impact_selection: true enables intelligent test selection, so Nova (or your CI) can run only tests impacted by the changes, speeding up re-test cycles.

You can adjust these settings based on your comfort level. For instance, if you fully trust Nova for certain kinds of changes, you can move them into the auto_commit list. The config ensures Nova fits your project's risk profile.

Contributing

Contributions to Nova are welcome! 🤝 If you have ideas, bug reports, or improvements, please open an issue or pull request. We encourage feedback and community involvement to make CI/CD fully autonomous and robust.

For major changes or proposals, consider starting a discussion first to align on design. Please ensure that any contributed code is covered by appropriate tests (Nova should help keep itself green, after all!). We plan to add a Contributing Guide with more details soon – including how to run Nova locally for development, coding style, and our CLA/License info.

Nova is on a mission to eliminate the pain of broken builds and slow, error-prone deployments. With Nova as your shipping copilot, every PR can arrive green and ready to merge – every PR shippable, automatically.

# AlwaysGreen — Self‑Healing CI/CD

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Actions/GitLab/Buildkite run your checks; AlwaysGreen makes them pass — safely, automatically.

Not a coding copilot. A shipping copilot.

AlwaysGreen is an autonomous CI/CD autopatcher. On every pull request, AlwaysGreen reproduces failures, maps them to likely fixes, proposes a minimal diff, commits on a safe side branch, and re‑runs your pipeline until the suite is green (or a safety limit is reached).

Result: PRs arrive shippable, with full auditability and guardrails.

> **Note**: This is the first public release of AlwaysGreen. Prior internal development history was not published to ensure a clean, secure, and professional open source launch.

## Table of Contents

- [Why AlwaysGreen?](#why-alwaysgreen)
- [What AlwaysGreen Does](#what-alwaysgreen-does)
- [How It Works (Autopatch Loop)](#how-it-works-autopatch-loop)
- [Quickstart](#quickstart)
  - [GitHub Actions](#github-actions)
  - [Local run](#local-run)
  - [Other CI (GitLab, Buildkite)](#other-ci-gitlab-buildkite)
- [Configuration](#configuration)
- [Metrics AlwaysGreen Improves](#metrics-nova-improves)
- [Roadmap](#roadmap)
- [What AlwaysGreen Is / Isn't](#what-alwaysgreen-is--isnt)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

## Why AlwaysGreen?

Editors have coding copilots (Copilot, Cursor, Claude Code). Shipping is still where velocity dies:

- Red builds, flaky tests, blocked merges.
- Hours of babysitting pipelines and parsing logs.
- Tools that alert and gate, but rarely act and repair.

Writing software is easy; shipping it safely at velocity is hard. AlwaysGreen closes the loop by not only detecting failures but fixing them automatically.

“Alerts are cheap; fixes are priceless. AlwaysGreen does both.”

## What AlwaysGreen Does

### PR Review + Auto‑Fix (v1)

- Summarizes failing checks and likely root causes.
- Proposes and commits minimal diffs on a safe branch (`nova/fix/...`).
- Re‑runs checks and iterates until green or limits are hit.
- Works even with light/no tests via lint/type/build/import fixes and generated smoke tests (optional).

### Safe by Default

- Never touches `main`.
- Risk budget & limits (files/LOC/attempts).
- One‑paragraph rationale, diff stats, and provenance in every patch.

### BYO Model

Bring your own API key (OpenAI / others). You stay in control.

## How It Works (Autopatch Loop)

- **Plan** — Classify the failure and draft a repair plan within a risk budget.
- **Generate** — Propose a minimal patch (e.g., LOCΔ ≤ 40) on a side branch.
- **Patch** — Apply changes to `nova/fix/...` (never `main`).
- **Critic** — Re‑run checks; if still failing, critique → loop.

Each patch includes: rationale, diff stats, provenance. Limits and risk policy keep changes reviewable and safe.

## Quickstart

### GitHub Actions

Create `.github/workflows/nova.yml`:

```yaml
name: AlwaysGreen CI Rescue
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
      - name: Run AlwaysGreen on this PR
        run: nova run --pr "${{ github.event.pull_request.number }}" --ci "pytest -q"
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

`--ci "pytest -q"` is your build/test command. Replace with whatever your pipeline runs.

### Local run

```bash
pip install nova-ci-rescue
export OPENAI_API_KEY=your-key-here   # your key
nova run --ci "pytest -q"
```

AlwaysGreen will run your checks, attempt minimal fixes on a local branch, and re‑run until green or limits are reached.

### Other CI (GitLab, Buildkite)

Install `nova-ci-rescue` in your CI job, then invoke:

```bash
nova run --ci "pytest -q"
```

AlwaysGreen works wherever your checks run. Use your CI’s secret manager to provide `OPENAI_API_KEY`.

## Configuration

Create `.github/nova.yml` (path is configurable) to set limits and risk policy:

```yaml
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
```

- **limits** — Safety rails that keep diffs small and reviewable.
- **risk** — Low‑risk categories may auto‑commit; riskier ones become suggestions for human review.
- **features**
  - `generate_smoke_tests`: synthesize tiny checks for uncovered critical paths.
  - `test_impact_selection`: run primarily impacted tests to speed iterations.

Tune these to your comfort level (e.g., move categories into `auto_commit` as trust grows).

## Metrics AlwaysGreen Improves

- Time‑to‑Green ↓
- % of Red PRs Auto‑Fixed ↑
- Accepted‑Diff Rate ↑
- Reviewer Babysitting Minutes ↓

Track these over time to quantify ROI.

## Roadmap

- **V1 (now)** — PR Auto‑Fix: minimal diffs for lint/type/build/test/import failures.
- **V2** — Policy & Test Synthesis: enforce conventions/security; generate missing micro‑tests.
- **V3** — Flake & Reliability Stabilizer: quarantine/rewrite flakies; optimize CI time.
- **V4** — Deploy Guardian: canary & SLO watch; auto‑rollback/forward; surgical PRs.

Endgame: A self‑healing CI/CD autopilot that keeps PR→prod green across any runner.

## What AlwaysGreen Is / Isn’t

- **Is**: An agentic reviewer/fixer that patches the obvious & repetitive breakages before humans look.
- **Isn’t**: An IDE coding assistant. AlwaysGreen focuses on shipping, not typing.
- **Is**: Safe, auditable, and conservative by default.
- **Isn’t**: A “big bang” refactorer; AlwaysGreen prefers minimal diffs with clear rationales.

## FAQ

**Do I need a big test suite?**
No. AlwaysGreen already helps with lint/type/import/build failures and can generate small smoke tests. More tests = more autopatch power.

**Will AlwaysGreen touch main?**
No. AlwaysGreen works on `nova/fix/...` (or your configured branch). You review/merge.

**What if a fix looks risky?**
Riskier categories land as suggestions (PR comments or draft commits). You stay in control via the risk policy.

**Which languages are supported?**
AlwaysGreen’s v1 flow is optimized for Python projects (e.g., pytest). Additional stacks are on the roadmap.

**Which models can I use?**
Bring your own API key (e.g., OpenAI). Configure via `OPENAI_API_KEY`. (Follow your model provider’s data policies.)

**How do I observe what AlwaysGreen changed?**
Each patch includes a one‑paragraph rationale, diff stats, and provenance. The CI logs also show AlwaysGreen’s plan/critic loop.

## Contributing

Contributions welcome!

- Open an issue or PR with repro steps and failing checks.
- Keep diffs minimal where possible (AlwaysGreen approves!).
- Larger proposals: start a discussion first.

We’ll add a full CONTRIBUTING guide and code of conduct shortly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT © AlwaysGreen contributors

---

Badges / Links

- Install: `pip install nova-ci-rescue`
- Taglines: "Not a coding copilot. A shipping copilot." · "Every PR shippable, automatically."

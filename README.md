# AlwaysGreen — Self‑Healing CI/CD

[![CI](https://github.com/alwaysgreenhq/alwaysgreen/workflows/CI/badge.svg)](https://github.com/alwaysgreenhq/alwaysgreen/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/alwaysgreen.svg)](https://badge.fury.io/py/alwaysgreen)

Actions/GitLab/Buildkite run your checks; AlwaysGreen makes them pass — safely, automatically.

Not a coding copilot. A shipping copilot.

AlwaysGreen is an autonomous CI/CD autopatcher. On every pull request, AlwaysGreen reproduces failures, maps them to likely fixes, proposes a minimal diff, commits on a safe side branch, and re‑runs your pipeline until the suite is green (or a safety limit is reached).

Result: PRs arrive shippable, with full auditability and guardrails.

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
- Taglines: “Not a coding copilot. A shipping copilot.” · “Every PR shippable, automatically.”

## Market One‑Pager

<!-- BEGIN: MARKET ONE-PAGER -->

# AlwaysGreen (AI CI/CD Fix Agent) – TAM & SAM Overview

AlwaysGreen is an AI-based CI/CD review and fix agent that automatically reviews pull requests, identifies failing checks (tests, builds, lint, policy), and pushes minimal patches to fix them. Below we estimate AlwaysGreen’s Total Addressable Market (TAM) and Serviceable Available Market (SAM) under two monetization models: a usage-based pricing (per fix) and an enterprise licensing (per team). The table summarizes annual market size, followed by key assumptions.

## TAM & SAM Estimates

| Market Size             | Usage-Based Model <br/>(per fix pricing)                                      | Enterprise Model <br/>(team licensing)                      |
| ----------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **TAM (Global)**        | ~\$100 M/year <br/><small>(mid-scenario; up to ~\$400 M in high-case)</small> | ~\$32 B/year <br/><small>(all dev teams globally)</small>   |
| **SAM (Initial focus)** | ~\$50 M/year <br/><small>(GitHub Actions users)</small>                       | ~\$24 B/year <br/><small>(teams on GitHub platform)</small> |

> (All figures are rough, back-of-envelope estimates.)

## Key Assumptions & Rationale

- **Developer Ecosystem Scale**: ~27 million software developers worldwide. We assume roughly 2.7 M dev teams (avg. ~10 developers per team). GitHub is the largest dev platform (100 M+ users), so distribution via GitHub Marketplace can reach a majority of the market initially.
- **CI/CD Usage Base**: GitHub Actions processes ~10.5 billion CI minutes per year (public repos). Extrapolating to include GitHub private repos and other CI providers (GitLab CI, CircleCI, Jenkins, etc.), we estimate ~30–40 B total CI minutes/year globally. GitHub Actions is used by ~53% of developers (Jenkins ~52%, GitLab CI ~35%), indicating GitHub accounts for roughly half of CI activity.
- **CI Failure Rate**: Assume ~2%–10% of all CI runs fail due to code issues that AlwaysGreen can automatically fix (failed tests, lint errors, etc.). We use a 5% failure rate as a midpoint for calculations.
- **Usage-Based Pricing Model**: Price at \$0.10–\$1.00 per automated fix. Mid-case: \$0.50 per fix. With ~4 B CI runs/year (from ~40 B minutes, assuming ~10 min per run) and a 5% fixable failure rate → ~200 M fixes/year → ~\$100 M TAM. High case (10% at \$1) ≈ ~\$400 M; low case (2% at \$0.10) < \$10 M.
- **Enterprise Licensing Model**: Annual team license ≈ \$1,000/mo per team (\$12K/year). With ~2.7 M addressable dev teams globally → \~\$32 B TAM. Focus on teams on GitHub (≈75% reach) → \~\$24 B SAM. Unlimited fixes per team under license captures more value vs per-fix.

**Bottom Line**: A usage-based model yields a modest TAM (tens of millions USD annually), whereas an enterprise SaaS model targets a multi-billion dollar market. GitHub Marketplace distribution enables large initial SAM, with expansion to other CI platforms over time.

---

# AlwaysGreen: Self‑Healing CI/CD — Market One‑Pager (Aug 30, 2025)

**One‑liner**

Actions/GitLab/Buildkite run your checks; AlwaysGreen makes them pass—safely, automatically.

## TL;DR

- **Fast‑growth budget lines**: AlwaysGreen sits where CI/CD & DevOps meet AIOps—markets compounding 19–22%+; faster than observability/testing (≈10–11%).
- **Massive user base & adoption**: ~19.6M professional devs; 47.2M total devs globally. 83% report involvement in DevOps/CI/CD activities.
- **Clear pain to monetize**: Main‑branch success averages ~82.5% (CircleCI), leaving failure/retry drag; flaky tests remain pervasive at scale.

## Core markets AlwaysGreen touches (size → forecast)

| Category                        | Base (\$B) | Base Year | Forecast / Horizon |              CAGR |
| ------------------------------- | ---------: | --------: | ------------------ | ----------------: |
| DevOps platforms                |      16.13 |      2025 | \$43.17B by 2030   |            21.76% |
| Continuous delivery (CI/CD)     |       3.67 |      2023 | to 2030            | 19.2% (2024–2030) |
| Automation testing              |      20.60 |      2025 | \$63.05B by 2032   | 17.3% (2025–2032) |
| AIOps platforms                 |       2.23 |      2025 | \$8.64B by 2032    | 21.4% (2025–2032) |
| Observability tools & platforms |       2.94 |      2024 | \$5.40B by 2030    | 10.7% (2024–2030) |
| Application security            |       33.7 |      2024 | \$55.0B by 2029    | 10.3% (2024–2029) |

> Notes: scopes overlap (don’t sum). Windows vary; use directionally to show tailwinds.

## Adjacent AI‑dev categories (end‑game autonomy relevance)

| Category                        | Base (\$B) | Base Year | Forecast / Horizon   |              CAGR |
| ------------------------------- | ---------: | --------: | -------------------- | ----------------: |
| AI in software development      |      0.674 |      2024 | \$15.7B by 2033      | 42.3% (2025–2033) |
| AI code assistants / code tools |   6.7–29.6 | 2024–2025 | \$25.7–97.9B by 2030 |      ~25% / 24.8% |

## Adoption & volume (Why now)

- **DevOps is mainstream**: 83% of developers report involvement in DevOps‑related activities.
- **Success isn’t universal**: Main‑branch success ~82.5% → room for automatic remediation.
- **Flakiness is endemic**: e.g., at scale, 1.5% of runs flaky; ~16% of individual tests exhibit flakiness.

## “Where the money is” (market proxies & adjacent spend)

- GitLab FY2025 revenue: \$759M (+31% YoY).
- Datadog 2024 revenue: \$2.68B; TTM to mid‑2025 \~\$3.02B (+26% YoY).
- CI tools market: \$1.73B (2025) → \$4.53B (2030).

## Implications for AlwaysGreen (numbers to quote)

- **Platform priority**: First‑class GitHub/Actions integration → direct reach into the largest CI share plus 10.54B annual CI minutes.
- **Concurrency is exploding**: 71% commit multiple times/day; 29% release multiple times/day → “always‑green PRs” is a daily problem.
- **AI appetite + trust gap**: 84% using AI tools but 46% distrust accuracy → emphasize explainable auto‑patches, minimal diffs, and “show your work.”

## Sources (selected)

CNCF Annual Survey 2024; GitHub Octoverse 2024; Stack Overflow Developer Survey 2025; GitHub Newsroom; Microsoft/TechCrunch (Copilot usage); GitLab IR; Datadog; Mordor Intelligence; Grand View Research; Fortune Business Insights; MarketsandMarkets; ResearchAndMarkets; JetBrains; SlashData; CircleCI State of Software Delivery; research on test flakiness (e.g., ICSE’20).

---

If helpful, I can harmonize all forecasts to a single window (e.g., 2025–2030) and add a PNG chart for the CAGRs.

<!-- END: MARKET ONE-PAGER -->

## Business Model & Pricing

<!-- BEGIN: BUSINESS MODEL -->

# AlwaysGreen Greenline™ — Business Model & Pricing

Below I'll (1) name the billion‑dollar model in one sentence, then (2) lay out a concrete business model you can ship from the GitHub Marketplace up through enterprise ELAs, with pricing, packaging, ROI math, GTM, and defensibility that aligns with your repo's story.

---

## 1) The billion‑dollar model in one sentence

> **Sell "always‑green shipping" as an org‑wide reliability platform**—a GitHub‑native app that automatically repairs broken PRs and enforces release SLOs—**priced as a team/enterprise license with a usage (fix‑credit) booster and an ROI guarantee.**

Why this scales:

- **Mass adoption + measurable pain.** CI "main branch" success averages ~**82.15%**, leaving a persistent failure tail your agent can remediate. Autopatching that tail is quantifiable dollars saved in compute + developer time.
- **DevOps is mainstream.** ~**83%** of developers participate in DevOps/CI/CD activities—the user base is there.
- **Favorable channel economics.** The **GitHub Marketplace takes only 5%**, leaving 95% to you, which supports PLG distribution and strong margins.

---

## 2) A complete business model you can run with

### A. Product → Packaging (good → better → best)

**Wedge (PLG): GitHub App — "AlwaysGreen CI Rescue" (Team‑ready)**

- **Promises**: On every PR, reproduce failure → propose a minimal patch → commit to a safe side branch → re‑run checks until green (within a risk budget).
- **Trust UX**: never touch `main`; show rationale, diff stats, provenance; configurable risk categories (auto‑commit vs suggest‑only).
- **Distribution**: GitHub Marketplace (simple install, SSO), with 14‑day trial.

**SKUs**

1. **Starter (App Store)** – Flat plan

   - For small teams/on‑ramps.
   - Includes **BYO LLM** (customer pays their model bill), basic guardrails, and **N** monthly **Fix Credits** (see pricing).
   - Extra Fix Credits available as in‑app top‑ups.

2. **Team (Pods of 10)** – Team license + credits

   - Adds "managed inference" (your model bill), advanced policy & audit, Slack/Jira hooks, test‑impact execution, and SSO.
   - Billed per **team pod** (≈10 devs), mapping to the way engineering orgs actually budget pods/squads.

3. **Enterprise (Org‑wide ELA)** – Unlimited & SLA
   - Org‑wide coverage, **on‑prem runner / private cloud**, custom risk policy, PII controls, audit ledger, and **Greenline SLA** (e.g., 90% of fixable reds auto‑remediated or credits back).
   - Seatless org pricing (ELA) + optional volume **Fix Credits** for bursty workloads.

> **Note on Marketplace rules**: GitHub supports flat‑rate and per‑unit (per‑user) pricing in Marketplace; usage‑only (per‑fix) billing isn't natively supported. The pattern that works: ship flat/per‑user plans that include a monthly Fix‑Credit allowance, with optional credit packs handled either as: (a) additional Marketplace plans or (b) direct billing (if you also list at least one paid Marketplace plan). GitHub remits 95% of Marketplace revenue to you.

### B. Pricing that aligns to value (and to how devtools are bought)

Anchor against what buyers already know:

- **Copilot** normalizes **$19–$39/user/mo** enterprise budgets.
- **Buildkite Pro** is **$30/active user/mo** and their Test Engine includes a **$0.10/test** usage component—so mixed seat + usage pricing is familiar.

**Recommended price points (launch):**

| Plan                    | What they get                                                                                      | Price (suggested)                                          |
| ----------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Starter (App Store)** | BYO‑LLM; 2,000 **Fix Credits**/mo; PR comments + safe‑branch patches; basic policy                 | **$299/org/mo**                                            |
| **Team (Pods of 10)**   | Managed inference; 10,000 **Fix Credits**/mo; SSO; Slack/Jira; test‑impact execution; policy packs | **$1,200/pod/mo** (=$12k/yr/pod)                           |
| **Enterprise ELA**      | Org‑wide, on‑prem / VPC option, unlimited attempts\*, Greenline SLA, custom policy/audit           | **$150k–$500k/yr** (by org size); \*soft‑cap with fair use |

**Overage**: additional **Fix Credits** @ **$0.25–$0.50/fix attempt** (down‑tiered by volume).
(You can start at $0.50 and step down at 100k+/mo.)

> **Why credits?** They map cleanly to your autopatch loop and to the cost to serve (compute + LLM). Buyers like "predictable base, elastic burst."

### C. ROI math that closes enterprise deals

Use public benchmarks to do a fast payback story in‑product:

- CircleCI's 2025 report shows **avg main‑branch success = 82.15%**, i.e., **17.85% failure** baseline. Suppose a customer runs **5,000 workflows/day**. Fails/day ≈ 5,000 × 17.85% = **893**. If AlwaysGreen auto‑fixes **30%** of those, that's **268** saves/day. At **30 minutes** engineer time per failure avoided and a loaded rate of **$120/hour**, that's **~$16,065/day** or **~$4.18M/year** saved (260 workdays). Even at 5–10% autofix rates, the payback remains obvious.

You can show similar ROI for smaller teams—e.g., **600 runs/day** yields **~$501k/year** in avoided toil at a 30% autofix rate.

**Monetize 10–20% of realized savings** and procurement will lean in.

### D. GTM: how to get from 0 → $100M ARR on the way to $1B

1. **Land via Marketplace (PLG)** with 95/5 rev split. Make install frictionless; auto‑detect failing checks, and show one "free save" during trial to prove value.
2. **Expand by pods.** Your packaging around **teams of ~10 devs** aligns to how engineering budgets and headcount grow—pods can add licenses independently.
3. **Upsell to Enterprise ELA** when you're protecting **main** and **release** branches org‑wide with policy packs, audit, and the Greenline SLA (exec‑friendly).
4. **Co‑sell with CI vendors** (GitHub, GitLab, Buildkite), SIs, and cloud marketplaces. Buildkite and Datadog both conditions buyers to mixed seat/usage pricing and "pipeline visibility" budgets; you're the **repair** counterpart.

### E. What exactly are "Fix Credits"?

A **Fix Credit** is one full autopatch attempt cycle on a PR (plan → patch → re‑run → critic).

- **Charge on attempt**, **refund** on obvious non‑actionables (e.g., external outage).
- Separate **"analyze‑only"** free tier (summarize failure, likely root causes) to keep the funnel wide.

### F. Enterprise features that justify the big check

- **Greenline SLA**: commitment that X% of fixable CI reds are auto‑remediated (by category) within Y minutes—or give **service credits**.
- **Risk policy & audit ledger:** regulators and security teams get a **verifiable record** of every bot action.
- **Guardrails**: never touch `main`; LOC/attempt caps; category‑gated auto‑commits (lint/format/import/type), suggestions for risky fixes (deps/schema/security).
- **Data governance**: on‑prem runners, model choice (BYO or managed), PII redaction, repo scoping.
- **Change accountability**: owners, diffs, provenance, and revert buttons.

### G. Moat: why this compounds defensibility

1. **Fix‑graph & heuristics corpus.** Each accepted patch enriches a private "fix library" (by stack/version/test name/error signature). Over time, AlwaysGreen becomes the default maintainer of **institutional CI knowledge**.
2. **Policy engine + auditability.** Compliance teams approve you as the **only** agent allowed to commit on CI failures under defined limits—this becomes sticky.
3. **Distribution lock‑in.** Marketplace presence, verified publisher status, and PR‑native UX (checks, comments, branch writes) are hard for new entrants to replicate quickly at quality.

### H. Risks & how to handle them (brief)

- **False positives / risky changes** → keep "risky categories" as **suggest‑only** until trust builds; clear rollbacks; diff stats & rationale in every patch.
- **LLM cost volatility** → dual model strategy (BYO or managed); knob to cap tokens per attempt; compression/cot pruning.
- **Marketplace constraints on usage billing** → sell **plans with included credits**; offer **credit add‑ons**; for very large customers, close **direct ELAs**.

---

## 3) Concrete pricing sheet you can publish tomorrow

### GitHub Marketplace listing

- **Starter** – $299/org/month – 2,000 Fix Credits/month, BYO LLM, safe‑branch patches, PR comments, basic policy & audit.
- **Team** – $1,200/pod/month (10 devs) – 10,000 Fix Credits/month, managed inference, SSO, Slack/Jira, test‑impact, advanced policy packs.
- **Credit add‑ons** – $0.50 per attempt (tiered down to $0.25 at 100k+/mo).

### Direct (Sales)

- **Enterprise ELA** – $150k–$500k/year – org‑wide; on‑prem/VPC; unlimited\* with fair use; Greenline SLA; custom policy; audit API; DLP/PII controls; premium support.
- Optional **savings‑share** rider (e.g., 5–10% of verified GitHub Actions compute **saved** vs baseline); keep as a lever only when procurement pushes for pay‑for‑outcomes. (You can estimate baselines from Actions usage metrics exports.)

---

## 4) 90‑day execution plan

### Week 0–2:

- Ship **Marketplace verified publisher** and **paid plans** (Starter/Team). (Marketplace requires annual + monthly prices and allows free trials.)
- In‑product **ROI panel** based on observed workflow counts and your fix‑acceptance rate (CSV usage imports optional).

### Week 3–6:

- **Design partners** (3–5 logos) on Enterprise preview—lock down policy packs and the audit ledger.
- Publish a **"State of CI Auto‑Repair"** blog with anonymized stats: % PR reds turned green; median time‑to‑green saved; top fix categories. Anchor it to CircleCI's 82% success baseline to show the slice you remove.

### Week 7–12:

- Launch **Greenline SLA** and announce **on‑prem runner**.
- Start **co‑marketing** with a CI vendor (Buildkite/GitHub Actions ecosystem partners). Buildkite's public pricing normalizes mixed license + usage—good adjacent narrative.

---

## 5) TL;DR—what to call it

**AlwaysGreen Greenline™ — the Release Reliability Platform.**

Actions/GitLab/Buildkite run your checks; AlwaysGreen makes them pass—and you only pay a predictable team license plus credits for the tough ones. (GitHub Marketplace gets 5%; you keep 95%.)

---

_If you want, I'll adapt this into (a) a pricing page draft and (b) a one‑slide sales ROI calculator you can drop into the repo's /docs._

<!-- END: BUSINESS MODEL -->

## Solution Audit & Technical Framing

<!-- BEGIN: SOLUTION AUDIT -->

# AlwaysGreen "Green-SLA" Shipping Copilot – Solution Audit and Framing

## Problem Context: Failing CI/CD Drains Velocity

Modern software teams often struggle with red builds, flaky tests, and broken pipelines that halt progress. A failing CI job means engineers spend hours babysitting pipelines – parsing logs, rerunning tests, and applying manual fixes. Current CI systems largely serve an alert-and-block role: they run tests and notify you of failures, but don't help fix the underlying issues. As a result, shipping velocity suffers; merges are delayed and developers lose focus context-switching to debug CI problems.

Why AlwaysGreen? The gap is clear – while editors have coding copilots to assist with writing code, there's no "shipping copilot" ensuring that code actually gets to production. This is the problem AlwaysGreen addresses: automatically turning failing pull requests into passing ones (or providing a bounded plan) so that every PR arrives shippable with minimal human intervention.

## Solution Overview: AlwaysGreen as a Self-Healing CI/CD Copilot

AlwaysGreen is proposed as an autonomous CI/CD autopatcher – essentially a "self-healing" layer for your pipeline. On each pull request (PR), AlwaysGreen will automatically:

1. Reproduce the failure in a hermetic environment (same dependencies, seeds, etc.),
2. Diagnose the root cause,
3. Plan a fix within strict safety limits,
4. Apply a minimal patch on a side branch, and
5. Re-run the tests to verify the fix.

It repeats this loop until the PR's checks go green or it reaches a defined attempt limit. If it cannot fix the issue, AlwaysGreen will post a detailed analysis and plan for a human to review. All of this happens as part of your CI flow, so by the time a developer looks at the PR, it's either already green or comes with a clear path to green.

In short, AlwaysGreen acts as a "shipping copilot": instead of just telling you something's wrong, it actively makes failing checks pass – safely and automatically. This turns the traditional CI promise into a "Green-SLA": an expectation that builds stay green by default, with AlwaysGreen doing everything possible to meet that standard.

## Mapping the Runbook to AlwaysGreen's Features

Teams often have a runbook for CI failures – a series of manual steps engineers follow when a build breaks. AlwaysGreen codifies that entire process into product features, creating a closed-loop, alert-first automation. For example:

- **"Stop the line"** (halt merges, notify team) – AlwaysGreen implements this via incident state + alerts (Slack notifications, GitHub check failures). If the main branch is broken, AlwaysGreen posts status updates and prevents further merges.

- **Reproduce in the same environment** – AlwaysGreen uses a hermetic test runner (consistent base images, pinned dependencies, fixed random seeds) to ensure it sees the exact same failure as CI.

- **Focus on first error** – AlwaysGreen includes a log parser that extracts the first failure or error signature, so it concentrates on the root cause rather than getting lost in cascading errors.

- **Time-box the investigation, then revert** – AlwaysGreen has an auto-revert policy: if it can't fix the build within a grace period or a couple of attempts, it can automatically roll back the offending commit (this is configurable and initially off until you're comfortable).

- **Bisect when cause is unclear** – AlwaysGreen provides an on-demand bisect job to pinpoint which commit introduced a failure. This isn't run every time, but you can trigger it (or even automate it) if a failure's cause isn't obvious.

- **Detect flakiness and quarantine** – AlwaysGreen includes a flake classifier that watches for tests that fail intermittently. It can label or quarantine flaky tests (e.g., move them out of required checks) so they don't keep spurious failures from blocking merges.

- **Apply the smallest safe fix** – AlwaysGreen's Green-SLA autopatcher tries to make the minimal change necessary (bounded by N attempts, F files, L lines of code) to resolve the failure. The focus is on small, surgical fixes that are easy to review.

- **Explain every change** – Every AlwaysGreen-generated patch comes with an explanation (a one-paragraph rationale) and links to relevant logs or artifacts. This way, developers can understand why the change was made.

- **Enforce guardrails** – AlwaysGreen uses policy-as-code (OPA/Rego) plus scanners to enforce rules (e.g. no touching certain sensitive files, respecting CODEOWNERS, limiting how much can change). These guardrails ensure AlwaysGreen's fixes stay within agreed boundaries.

By mapping the manual runbook steps to these capabilities, AlwaysGreen ensures that the entire CI failure-handling process is owned end-to-end by automation. What used to be a page of instructions in a Wiki is now baked into the CI/CD pipeline itself.

## Key Components and Configuration

AlwaysGreen's solution is delivered through a combination of config-as-code, CI pipeline hooks, and lightweight CLI tools/scripts. The major components include:

### AlwaysGreen Configuration (nova.yml)

A file (e.g. `.github/nova.yml`) in the repo defines AlwaysGreen's operating limits and policies. For example, you can set limits like `max_attempts: 2` (AlwaysGreen will try at most 2 patches), `max_files_changed: 5`, `max_loc_delta: 40` (no patch bigger than 40 lines added/removed) etc. It also defines risk categories – e.g., AlwaysGreen might auto-commit safe fixes (linting, formatting, simple type errors) but only suggest changes for higher-risk issues (dependency upgrades, major refactors).

The config also lists alert channels and rules (Slack, GitHub comments, PagerDuty escalation) and policy settings (like which paths are protected, whether to enforce CODEOWNERS checks, etc.). All these settings make AlwaysGreen's behavior transparent and tunable via versioned code.

### GitHub Actions Workflows

AlwaysGreen integrates into CI via standard workflows. The solution provides ready-to-use YAML workflows:

**PR Auto-Fix Workflow** (e.g., `.github/workflows/nova-ci-rescue.yml`): This runs on every pull request update. It checks out the code, ensures the environment is ready (using a preflight script), then invokes AlwaysGreen's CLI (for example: `nova run --pr $PR_NUMBER --ci "pytest -q"`). AlwaysGreen then attempts to fix any test failures on that PR. If AlwaysGreen makes changes, it commits them to a new branch (like `nova/fix/123` for PR #123) and pushes, so the PR picks up the changes.

**Main Branch Guardian Workflow** (`nova-main-guardian.yml`): This runs on pushes to the main branch (or whatever the "protected" branch is). It executes the test suite in a controlled way (capturing the first error to a log). If the suite fails, this workflow will handle incident response: it can create a GitHub Check run that shows the failure, post a Slack alert to notify the team that the main branch is broken, and optionally trigger a PagerDuty escalation if no one responds in a given time.

**On-Demand Bisect Workflow** (`nova-bisect.yml`): This is a manually-triggered (`workflow_dispatch`) job that takes inputs (a "good" last-known-green SHA, a "bad" current SHA, and a test command). It uses `git bisect` under the hood to automatically run the failing test on different commits to pinpoint which commit introduced a failure.

### Utility Scripts

Alongside the workflows, AlwaysGreen provides scripts to assist in the CI environment:

- `scripts/ci/preflight.sh` – This runs before AlwaysGreen's main logic. It checks that the environment is sane and sets consistent environment settings.
- `scripts/ci/first_error.sh` – Given a full CI log, this script finds the first occurrence of a failure and prints that section.
- `scripts/ci/env_fingerprint.sh` – This gathers information about the environment and dependencies and writes it to an artifact file.

### Guardrail Policies (OPA/Rego)

The solution includes a policy file `policy/guardrails.rego` which encodes organization-specific rules for patches. AlwaysGreen's orchestrator can query this policy before applying any fix. For example, the policy might say:

- "If more than 5 files are changed or more than 40 lines are added/removed, that's a violation (too large of a fix)."
- "If the diff touches any file in `migrations/` or `secrets/` or other sensitive directories, that's a violation."
- "If multiple distinct areas are changed in one patch, flag it."

If any such rule is violated, AlwaysGreen will not auto-commit the patch; instead, it can either skip that fix or mark it for human review.

### Alerts and Notifications

AlwaysGreen is designed to integrate with team communication channels:

**Slack**: You can configure a Slack webhook in the AlwaysGreen config. The solution provides a sample shell script (`alerts/slack_payload.sh`) that formats a message with an emoji/status and a direct link to the relevant CI run or PR, then POSTs it to Slack.

**PagerDuty (PD)**: For critical pipelines (like prod deploys), AlwaysGreen can escalate to PagerDuty after a certain time. The config's alert rules allow an `escalate_after_minutes: X` setting.

**GitHub Checks and PR comments**: AlwaysGreen leverages GitHub's status checks API. For instance, the "AlwaysGreen CI Rescue" workflow can create a check run that reports the status of AlwaysGreen's attempts. If AlwaysGreen fails to fix a PR, it can mark the check as "action required" and attach logs or the plan for fixing.

All these components work together: the workflows trigger AlwaysGreen at the right times, the config and policies constrain its behavior, and the scripts plus integration hooks let AlwaysGreen communicate what it's doing.

## Autopatch Loop Mechanism: "Plan → Patch → Verify"

At the heart of AlwaysGreen is an autopatch loop that embodies the "reproduce and repair" cycle:

1. **Reproduce & Capture**: AlwaysGreen starts by running the test suite (or specific failing checks) in an isolated environment to see the failure firsthand. It captures the logs, and using the `first_error.sh` logic, identifies the first point of failure.

2. **Plan**: Based on the failure classification and AlwaysGreen's internal knowledge base, it formulates a repair plan. The plan is essentially: "What minimal change could fix this?" AlwaysGreen always stays within the risk budget defined – e.g., "At most 2 attempts for this PR, touching no more than 5 files and adding/removing ≤ 40 lines total."

3. **Generate Patch**: AlwaysGreen then uses AI (and possibly some templated fixes for known issues) to generate the code changes according to the plan. This could involve editing a few lines in a function, adding a small test, updating a version in a config file, etc. The emphasis is on minimality – the smallest possible diff that could resolve the failure.

4. **Apply to Side Branch**: AlwaysGreen never commits directly to main. It commits the patch to a separate branch (e.g., `nova/fix/<PR-number>` or a similarly prefixed branch). This approach means that the original PR branch isn't altered by AlwaysGreen – instead, the PR is updated via a new commit from AlwaysGreen on a side branch.

5. **Run Tests on the Patch**: After applying the patch, AlwaysGreen triggers the CI checks again. Now we see if the fix worked. If all tests pass, wonderful – AlwaysGreen has managed to turn the PR green. If there's still a failure (or a new failure), AlwaysGreen records that outcome for the next iteration.

6. **Critique & Iterate**: If the tests are still failing, AlwaysGreen goes back to step 1 or 2: it analyzes the new failure and will then come up with a refined plan or a new plan for the new error. AlwaysGreen will iterate this cycle, but only up to a fixed number of attempts (`max_attempts`) to avoid an infinite loop.

7. **Decide & Report**: After either succeeding or exhausting attempts, AlwaysGreen makes a decision:

   - **Success**: AlwaysGreen will update the PR with the fix branch commit(s) and typically add a comment like "✅ AlwaysGreen auto-fix applied: all checks are now passing."
   - **Failure/Exceeded Budget**: If AlwaysGreen couldn't fix the issue within the set attempts, AlwaysGreen will comment with a failure report and attach artifacts.

8. **Explain**: A key part of AlwaysGreen's philosophy is explainability. Each AlwaysGreen-generated patch comes with a one-paragraph rationale explaining why the change was made and evidence that it's safe.

Throughout this loop, AlwaysGreen is constrained by guardrails and policy at every step. It won't, for example, decide to pull in a new library or make a database schema change as a fix – those are beyond its scope unless explicitly allowed.

## Safety and Guardrails

AlwaysGreen's design prioritizes safety and control, recognizing that teams need to trust it gradually. Key safety mechanisms include:

- **No direct commits to main**: All fixes go to a `nova/fix/...` branch, keeping the primary branch untouched.
- **Strict change budgets**: AlwaysGreen enforces quantitative limits on its fixes (max files/LOC changed, max attempts).
- **Protected areas**: Certain files or directories can be declared off-limits or sensitive.
- **CODEOWNERS enforcement**: AlwaysGreen can be set to respect your repo's CODEOWNERS rules.
- **Policy-driven guardrails**: The OPA/Rego policy file encodes rules in a single source of truth.
- **Risk-tiered actions**: Not all fixes are equal. AlwaysGreen categorizes fixes by risk (low/medium/high-risk).
- **Human oversight for exceptions**: If AlwaysGreen hits a guardrail, it will defer to humans.

## Incident Handling and Alerting

AlwaysGreen treats CI failures as first-class incidents that need both attention and action:

**Main branch failures**: When a commit to main causes a red build, AlwaysGreen's Main Guardian comes into play. It will immediately surface the issue via multiple channels and can automatically pause any merge queues or deployment pipelines.

**Pull request failures**: When a PR's CI is failing, AlwaysGreen's PR Auto-Fix workflow will try to fix it. While doing so, it can post status updates and notify on Slack as well.

**Alert tuning**: Not every failed test needs a loud alert. The AlwaysGreen config allows tuning what conditions trigger which alerts.

## On-Demand Tools: Bisect and Flake Management

Two special cases in CI failures are when the cause is unknown and when the cause is intermittent (flaky tests). AlwaysGreen includes tools for both:

**Automated Bisect**: AlwaysGreen has a workflow to automate `git bisect`. If you supply a range and a command that determines "good vs bad", AlwaysGreen will binary-search through your commit history to find exactly which commit introduced the failure.

**Flake Detection & Quarantine**: AlwaysGreen's orchestrator can identify patterns where a test fails but on re-run passes. For known flaky tests, AlwaysGreen can automatically quarantine them.

## Adoption Path and Rollout Stages

Introducing an autonomous tool into CI/CD should be done carefully. AlwaysGreen's solution is designed to be adoptable in stages:

- **M0 – Explain-Only Mode**: Start with AlwaysGreen not making any changes at all. AlwaysGreen will analyze failures but only output explanations and possible solutions.
- **M1 – Automatic Small Fixes**: Allow AlwaysGreen to auto-fix very low-risk issues like lint errors and simple test assertions.
- **M2 – Moderate Fixes & Multi-File Changes**: AlwaysGreen tackles more complex issues within a contained scope.
- **M3 – Flake & Stability Management**: AlwaysGreen becomes proactive about the health of the test suite itself.
- **M4 – Deploy Guardian**: AlwaysGreen's self-healing extends into the deployment phase.

## Value Proposition and Differentiation

AlwaysGreen is positioned not as a traditional CI tool or a generic coding assistant, but as a new kind of outcome-focused CI companion:

- **Core Promise (Green-SLA)**: AlwaysGreen aims for "green by default" CI – it will do everything possible (within safe limits) to get a failing build back to green.
- **Outcome-Focused vs Tool-Focused**: Unlike traditional CI/CD tools that stop at running tests and reporting failures, AlwaysGreen actually acts to resolve those failures.
- **Minimal & Safe Fixes**: AlwaysGreen's fixes are intentionally small and auditable. Each patch is constrained in size and comes with an explanation and evidence.
- **Safety & Control**: A huge part of AlwaysGreen's differentiation is the safety layer with policies, config, and human approvals built-in.

## Operational Details and Evidence

The described GitHub Actions workflows and scripts are straightforward to implement. They follow best practices and give AlwaysGreen the needed permissions to push fix branches and update PRs. The use of hermetic test runs, first error focus, minimal patch strategy, and guardrails via Rego all show technical soundness.

The solution appears technically feasible and robust, covering the full spectrum from detection to fix to notification. Each piece is built on proven practices, which increases the likelihood that AlwaysGreen can be adopted without a huge learning curve.

## Product Framing and Language

In positioning AlwaysGreen, it's important to convey that this is not just another CI tool, but a new category of developer assistant focused on shipping quality code faster:

- **Category Name**: Self-Healing CI/CD
- **Role**: Shipping Copilot
- **Core Promise**: Green-SLA
- **Unit of Value**: "Minutes to Green" and "% PRs Auto-Fixed"
- **Patch Style**: "minimal, auditable diffs"
- **Risk Layer**: "policy-driven guardrails"

## Conclusion

The AlwaysGreen "Green-SLA Shipping Copilot" solution provides a comprehensive answer to the problem of failing CI pipelines by automating the diagnosis and repair process with safety and accountability. The audit shows that it covers all the critical bases: effectiveness, safety, transparency, completeness, adaptability, and vision.

If implemented and calibrated correctly, AlwaysGreen could significantly improve engineering productivity and confidence in the CI/CD process. It represents a promising step towards truly self-healing pipelines that change the mindset from "oh no, the build is red, who's going to fix it?" to "the build is red, but AlwaysGreen is on it – it might be green by the time I get back from lunch."

<!-- END: SOLUTION AUDIT -->

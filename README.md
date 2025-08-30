# Nova — Self‑Healing CI/CD

Actions/GitLab/Buildkite run your checks; Nova makes them pass — safely, automatically.

Not a coding copilot. A shipping copilot.

Nova is an autonomous CI/CD autopatcher. On every pull request, Nova reproduces failures, maps them to likely fixes, proposes a minimal diff, commits on a safe side branch, and re‑runs your pipeline until the suite is green (or a safety limit is reached).

Result: PRs arrive shippable, with full auditability and guardrails.

## Table of Contents
- [Why Nova?](#why-nova)
- [What Nova Does](#what-nova-does)
- [How It Works (Autopatch Loop)](#how-it-works-autopatch-loop)
- [Quickstart](#quickstart)
  - [GitHub Actions](#github-actions)
  - [Local run](#local-run)
  - [Other CI (GitLab, Buildkite)](#other-ci-gitlab-buildkite)
- [Configuration](#configuration)
- [Metrics Nova Improves](#metrics-nova-improves)
- [Roadmap](#roadmap)
- [What Nova Is / Isn’t](#what-nova-is--isnt)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

## Why Nova?

Editors have coding copilots (Copilot, Cursor, Claude Code). Shipping is still where velocity dies:

- Red builds, flaky tests, blocked merges.
- Hours of babysitting pipelines and parsing logs.
- Tools that alert and gate, but rarely act and repair.

Writing software is easy; shipping it safely at velocity is hard. Nova closes the loop by not only detecting failures but fixing them automatically.

“Alerts are cheap; fixes are priceless. Nova does both.”

## What Nova Does

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
      - name: Run Nova on this PR
        run: nova run --pr "${{ github.event.pull_request.number }}" --ci "pytest -q"
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

`--ci "pytest -q"` is your build/test command. Replace with whatever your pipeline runs.

### Local run
```bash
pip install nova-ci-rescue
export OPENAI_API_KEY=sk-...   # your key
nova run --ci "pytest -q"
```

Nova will run your checks, attempt minimal fixes on a local branch, and re‑run until green or limits are reached.

### Other CI (GitLab, Buildkite)
Install `nova-ci-rescue` in your CI job, then invoke:

```bash
nova run --ci "pytest -q"
```

Nova works wherever your checks run. Use your CI’s secret manager to provide `OPENAI_API_KEY`.

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

## Metrics Nova Improves

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

## What Nova Is / Isn’t

- **Is**: An agentic reviewer/fixer that patches the obvious & repetitive breakages before humans look.
- **Isn’t**: An IDE coding assistant. Nova focuses on shipping, not typing.
- **Is**: Safe, auditable, and conservative by default.
- **Isn’t**: A “big bang” refactorer; Nova prefers minimal diffs with clear rationales.

## FAQ

**Do I need a big test suite?**
No. Nova already helps with lint/type/import/build failures and can generate small smoke tests. More tests = more autopatch power.

**Will Nova touch main?**
No. Nova works on `nova/fix/...` (or your configured branch). You review/merge.

**What if a fix looks risky?**
Riskier categories land as suggestions (PR comments or draft commits). You stay in control via the risk policy.

**Which languages are supported?**
Nova’s v1 flow is optimized for Python projects (e.g., pytest). Additional stacks are on the roadmap.

**Which models can I use?**
Bring your own API key (e.g., OpenAI). Configure via `OPENAI_API_KEY`. (Follow your model provider’s data policies.)

**How do I observe what Nova changed?**
Each patch includes a one‑paragraph rationale, diff stats, and provenance. The CI logs also show Nova’s plan/critic loop.

## Contributing

Contributions welcome!

- Open an issue or PR with repro steps and failing checks.
- Keep diffs minimal where possible (Nova approves!).
- Larger proposals: start a discussion first.

We’ll add a full CONTRIBUTING guide and code of conduct shortly.

## License

MIT © Nova contributors

---

Badges / Links

- Install: `pip install nova-ci-rescue`
- Taglines: “Not a coding copilot. A shipping copilot.” · “Every PR shippable, automatically.”

## Market One‑Pager
<!-- BEGIN: MARKET ONE-PAGER -->
# Nova (AI CI/CD Fix Agent) – TAM & SAM Overview

Nova is an AI-based CI/CD review and fix agent that automatically reviews pull requests, identifies failing checks (tests, builds, lint, policy), and pushes minimal patches to fix them. Below we estimate Nova’s Total Addressable Market (TAM) and Serviceable Available Market (SAM) under two monetization models: a usage-based pricing (per fix) and an enterprise licensing (per team). The table summarizes annual market size, followed by key assumptions.

## TAM & SAM Estimates

| Market Size | Usage-Based Model <br/>(per fix pricing) | Enterprise Model <br/>(team licensing) |
|---|---|---|
| **TAM (Global)** | ~\$100 M/year <br/><small>(mid-scenario; up to ~\$400 M in high-case)</small> | ~\$32 B/year <br/><small>(all dev teams globally)</small> |
| **SAM (Initial focus)** | ~\$50 M/year <br/><small>(GitHub Actions users)</small> | ~\$24 B/year <br/><small>(teams on GitHub platform)</small> |

> (All figures are rough, back-of-envelope estimates.)

## Key Assumptions & Rationale

- **Developer Ecosystem Scale**: ~27 million software developers worldwide. We assume roughly 2.7 M dev teams (avg. ~10 developers per team). GitHub is the largest dev platform (100 M+ users), so distribution via GitHub Marketplace can reach a majority of the market initially.
- **CI/CD Usage Base**: GitHub Actions processes ~10.5 billion CI minutes per year (public repos). Extrapolating to include GitHub private repos and other CI providers (GitLab CI, CircleCI, Jenkins, etc.), we estimate ~30–40 B total CI minutes/year globally. GitHub Actions is used by ~53% of developers (Jenkins ~52%, GitLab CI ~35%), indicating GitHub accounts for roughly half of CI activity.
- **CI Failure Rate**: Assume ~2%–10% of all CI runs fail due to code issues that Nova can automatically fix (failed tests, lint errors, etc.). We use a 5% failure rate as a midpoint for calculations.
- **Usage-Based Pricing Model**: Price at \$0.10–\$1.00 per automated fix. Mid-case: \$0.50 per fix. With ~4 B CI runs/year (from ~40 B minutes, assuming ~10 min per run) and a 5% fixable failure rate → ~200 M fixes/year → ~\$100 M TAM. High case (10% at \$1) ≈ ~\$400 M; low case (2% at \$0.10) < \$10 M.
- **Enterprise Licensing Model**: Annual team license ≈ \$1,000/mo per team (\$12K/year). With ~2.7 M addressable dev teams globally → \~\$32 B TAM. Focus on teams on GitHub (≈75% reach) → \~\$24 B SAM. Unlimited fixes per team under license captures more value vs per-fix.

**Bottom Line**: A usage-based model yields a modest TAM (tens of millions USD annually), whereas an enterprise SaaS model targets a multi-billion dollar market. GitHub Marketplace distribution enables large initial SAM, with expansion to other CI platforms over time.

---

# Nova: Self‑Healing CI/CD — Market One‑Pager (Aug 30, 2025)

**One‑liner**

Actions/GitLab/Buildkite run your checks; Nova makes them pass—safely, automatically.

## TL;DR

- **Fast‑growth budget lines**: Nova sits where CI/CD & DevOps meet AIOps—markets compounding 19–22%+; faster than observability/testing (≈10–11%).
- **Massive user base & adoption**: ~19.6M professional devs; 47.2M total devs globally. 83% report involvement in DevOps/CI/CD activities.
- **Clear pain to monetize**: Main‑branch success averages ~82.5% (CircleCI), leaving failure/retry drag; flaky tests remain pervasive at scale.

## Core markets Nova touches (size → forecast)

| Category | Base (\$B) | Base Year | Forecast / Horizon | CAGR |
|---|---:|---:|---|---:|
| DevOps platforms | 16.13 | 2025 | \$43.17B by 2030 | 21.76% |
| Continuous delivery (CI/CD) | 3.67 | 2023 | to 2030 | 19.2% (2024–2030) |
| Automation testing | 20.60 | 2025 | \$63.05B by 2032 | 17.3% (2025–2032) |
| AIOps platforms | 2.23 | 2025 | \$8.64B by 2032 | 21.4% (2025–2032) |
| Observability tools & platforms | 2.94 | 2024 | \$5.40B by 2030 | 10.7% (2024–2030) |
| Application security | 33.7 | 2024 | \$55.0B by 2029 | 10.3% (2024–2029) |

> Notes: scopes overlap (don’t sum). Windows vary; use directionally to show tailwinds.

## Adjacent AI‑dev categories (end‑game autonomy relevance)

| Category | Base (\$B) | Base Year | Forecast / Horizon | CAGR |
|---|---:|---:|---|---:|
| AI in software development | 0.674 | 2024 | \$15.7B by 2033 | 42.3% (2025–2033) |
| AI code assistants / code tools | 6.7–29.6 | 2024–2025 | \$25.7–97.9B by 2030 | ~25% / 24.8% |

## Adoption & volume (Why now)

- **DevOps is mainstream**: 83% of developers report involvement in DevOps‑related activities.
- **Success isn’t universal**: Main‑branch success ~82.5% → room for automatic remediation.
- **Flakiness is endemic**: e.g., at scale, 1.5% of runs flaky; ~16% of individual tests exhibit flakiness.

## “Where the money is” (market proxies & adjacent spend)

- GitLab FY2025 revenue: \$759M (+31% YoY).
- Datadog 2024 revenue: \$2.68B; TTM to mid‑2025 \~\$3.02B (+26% YoY).
- CI tools market: \$1.73B (2025) → \$4.53B (2030).

## Implications for Nova (numbers to quote)

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
# Nova Greenline™ — Business Model & Pricing

Absolutely—there’s a very real **billion‑dollar business** sitting inside Nova’s “self‑healing CI/CD” wedge.

Below I’ll (1) name the billion‑dollar model in one sentence, then (2) lay out a concrete business model you can ship from the GitHub Marketplace up through enterprise ELAs, with pricing, packaging, ROI math, GTM, and defensibility that aligns with your repo’s story.

---

## 1) The billion‑dollar model in one sentence

> **Sell “always‑green shipping” as an org‑wide reliability platform**—a GitHub‑native app that automatically repairs broken PRs and enforces release SLOs—**priced as a team/enterprise license with a usage (fix‑credit) booster and an ROI guarantee.**

Why this scales:

* **Mass adoption + measurable pain.** CI “main branch” success averages ~**82.15%**, leaving a persistent failure tail your agent can remediate. Autopatching that tail is quantifiable dollars saved in compute + developer time.
* **DevOps is mainstream.** ~**83%** of developers participate in DevOps/CI/CD activities—the user base is there. ([CD Foundation][1], [DevOps.com][2])
* **Favorable channel economics.** The **GitHub Marketplace takes only 5%**, leaving 95% to you, which supports PLG distribution and strong margins. ([GitHub Docs][3], [The GitHub Blog][4])

---

## 2) A complete business model you can run with

### A. Product → Packaging (good → better → best)

**Wedge (PLG): GitHub App — “Nova CI Rescue” (Team‑ready)**

* **Promises**: On every PR, reproduce failure → propose a minimal patch → commit to a safe side branch → re‑run checks until green (within a risk budget).
* **Trust UX**: never touch `main`; show rationale, diff stats, provenance; configurable risk categories (auto‑commit vs suggest‑only).
* **Distribution**: GitHub Marketplace (simple install, SSO), with 14‑day trial.

**SKUs**

1. **Starter (App Store)** – Flat plan
   * For small teams/on‑ramps.
   * Includes **BYO LLM** (customer pays their model bill), basic guardrails, and **N** monthly **Fix Credits** (see pricing).
   * Extra Fix Credits available as in‑app top‑ups.

2. **Team (Pods of 10)** – Team license + credits
   * Adds “managed inference” (your model bill), advanced policy & audit, Slack/Jira hooks, test‑impact execution, and SSO.
   * Billed per **team pod** (~10 devs), mapping to the way engineering orgs actually budget pods/squads.

3. **Enterprise (Org‑wide ELA)** – Unlimited & SLA
   * Org‑wide coverage, **on‑prem runner / private cloud**, custom risk policy, PII controls, audit ledger, and **Greenline SLA** (e.g., 90% of fixable reds auto‑remediated or credits back).
   * Seatless org pricing (ELA) + optional volume **Fix Credits** for bursty workloads.

> Note on Marketplace rules: GitHub supports flat‑rate and per‑unit (per‑user) pricing in Marketplace; usage‑only (per‑fix) billing isn’t natively supported. The pattern that works: ship flat/per‑user plans that include a monthly Fix‑Credit allowance, with optional credit packs handled either as: (a) additional Marketplace plans or (b) direct billing (if you also list at least one paid Marketplace plan). GitHub remits 95% of Marketplace revenue to you. ([GitHub Docs][5])

### B. Pricing that aligns to value (and to how devtools are bought)

Anchor against what buyers already know:

* **Copilot** normalizes **$19–$39/user/mo** enterprise budgets. ([GitHub Docs][6], [GitHub][7])
* **Buildkite Pro** is **$30/active user/mo** and their Test Engine includes a **$0.10/test** usage component—so mixed seat + usage pricing is familiar. ([Buildkite][8])

**Recommended price points (launch):**

| Plan | What they get | Price (suggested) |
|---|---|---|
| **Starter (App Store)** | BYO‑LLM; 2,000 **Fix Credits**/mo; PR comments + safe‑branch patches; basic policy | **$299/org/mo** |
| **Team (Pods of 10)** | Managed inference; 10,000 **Fix Credits**/mo; SSO; Slack/Jira; test‑impact execution; policy packs | **$1,200/pod/mo** (= $12k/yr/pod) |
| **Enterprise ELA** | Org‑wide, on‑prem / VPC option, unlimited attempts*, Greenline SLA, custom policy/audit | **$150k–$500k/yr** (by org size); *soft‑cap with fair use |

Overage: additional **Fix Credits** @ **$0.25–$0.50/fix attempt** (down‑tiered by volume).

> Why credits? They map cleanly to your autopatch loop and to the cost to serve (compute + LLM). Buyers like “predictable base, elastic burst.”

### C. ROI math that closes enterprise deals

Use public benchmarks to do a fast payback story in‑product:

* CircleCI’s 2025 report shows **avg main‑branch success = 82.15%**. Suppose a customer runs **5,000 workflows/day**. Fails/day ≈ 5,000 × 17.85% = **893**. If Nova auto‑fixes **30%** of those, that’s **268** saves/day. At **30 minutes** per failure avoided and a loaded rate of **$120/hour**, that’s **~$16,065/day** or **~$4.18M/year** saved (260 workdays). Even at 5–10% autofix rates, the payback remains obvious.

You can show similar ROI for smaller teams—e.g., **600 runs/day** yields **~$501k/year** in avoided toil at a 30% autofix rate.

Monetize 10–20% of realized savings and procurement will lean in.

### D. GTM: how to get from 0 → $100M ARR on the way to $1B

1. Land via Marketplace (PLG) with 95/5 rev split. Make install frictionless; auto‑detect failing checks, and show one “free save” during trial to prove value. ([GitHub Docs][3])
2. Expand by pods. Packaging around **teams of ~10 devs** aligns to how engineering budgets grow—pods can add licenses independently.
3. Upsell to Enterprise ELA when you’re protecting **main** and **release** branches org‑wide with policy packs, audit, and the Greenline SLA.
4. Co‑sell with CI vendors (GitHub, GitLab, Buildkite), SIs, and cloud marketplaces. Buildkite and Datadog both condition buyers to mixed seat/usage pricing and “pipeline visibility” budgets; you’re the **repair** counterpart. ([Buildkite][8], [Datadog][9])

### E. What exactly are “Fix Credits”?

A **Fix Credit** is one full autopatch attempt cycle on a PR (plan → patch → re‑run → critic).

* Charge on attempt, refund on obvious non‑actionables (e.g., external outage).
* Separate **analyze‑only** free tier (summarize failure, likely root causes) to keep the funnel wide.

### F. Enterprise features that justify the big check

* **Greenline SLA**: commitment that X% of fixable CI reds are auto‑remediated within Y minutes—or give service credits.
* **Risk policy & audit ledger:** verifiable record of every bot action.
* **Guardrails**: never touch `main`; LOC/attempt caps; category‑gated auto‑commits (lint/format/import/type), suggestions for risky fixes (deps/schema/security).
* **Data governance**: on‑prem runners, model choice (BYO or managed), PII redaction, repo scoping.
* **Change accountability**: owners, diffs, provenance, and revert buttons.

### G. Moat: why this compounds defensibility

1. **Fix‑graph & heuristics corpus.** Each accepted patch enriches a private “fix library” (by stack/version/test name/error signature).
2. **Policy engine + auditability.** Compliance approves you as the **only** agent allowed to commit on CI failures under limits—sticky.
3. **Distribution lock‑in.** Marketplace presence, verified publisher, and PR‑native UX are hard to replicate quickly at quality. ([GitHub Docs][5])

### H. Risks & how to handle them (brief)

* **False positives / risky changes** → keep “risky categories” as **suggest‑only** until trust builds; rollbacks; diff stats & rationale in every patch.
* **LLM cost volatility** → dual model strategy (BYO or managed); token caps; compression/CoT pruning.
* **Marketplace constraints on usage billing** → sell **plans with included credits**; offer **credit add‑ons**; for very large customers, close **direct ELAs**. ([GitHub Docs][5])

---

## 3) Concrete pricing sheet you can publish tomorrow

**GitHub Marketplace listing**

* **Starter** – $299/org/month – 2,000 Fix Credits/month, BYO LLM, safe‑branch patches, PR comments, basic policy & audit.
* **Team** – $1,200/pod/month (10 devs) – 10,000 Fix Credits/month, managed inference, SSO, Slack/Jira, test‑impact, advanced policy packs.
* **Credit add‑ons** – $0.50 per attempt (tiered down to $0.25 at 100k+/mo).

**Direct (Sales)**

* **Enterprise ELA** – $150k–$500k/year – org‑wide; on‑prem/VPC; unlimited* with fair use; Greenline SLA; custom policy; audit API; DLP/PII controls; premium support.
* Optional **savings‑share** rider (e.g., 5–10% of verified GitHub Actions compute saved vs baseline).

---

## 4) 90‑day execution plan (outline)

**Week 0–2:**

* Ship Marketplace verified publisher and paid plans (Starter/Team). (Marketplace requires annual + monthly prices and allows free trials.)
* In‑product ROI panel based on observed workflow counts and your fix‑acceptance rate.

**Week 3–6:**

* Design partners (3–5 logos); instrument “Greenline SLA” pilot.
* Build “Fix Credits” metering and reporting; Slack/Jira integrations.

**Week 7–12:**

* Sales playbook for Team → Enterprise upgrades; security review kit; SOC2 plan.
* Co‑marketing with CI vendors; add cloud marketplace listings.

---

[1]: https://cd.foundation/reports/
[2]: https://devops.com/
[3]: https://docs.github.com/marketplace
[4]: https://github.blog/
[5]: https://docs.github.com/marketplace/selling-your-app
[6]: https://docs.github.com/copilot
[7]: https://github.com/features/copilot
[8]: https://buildkite.com/
[9]: https://www.datadoghq.com/
[10]: https://docs.github.com/actions
[11]: https://docs.github.com/billing/managing-billing-for-github-actions/about-billing-for-github-actions
<!-- END: BUSINESS MODEL -->

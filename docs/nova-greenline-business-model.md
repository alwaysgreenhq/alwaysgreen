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

# Configuration

AlwaysGreen is configured via environment variables (e.g., `.env`).

## Core

- OPENAI_API_KEY: API key for OpenAI (optional if using Anthropic)
- ANTHROPIC_API_KEY: API key for Anthropic (optional if using OpenAI)
- ALWAYSGREEN_DEFAULT_LLM_MODEL: e.g., `gpt-4o`, `gpt-5`, `claude-3-5-sonnet`
- ALWAYSGREEN_REASONING_EFFORT: reasoning effort for GPT models (`low`, `medium`, `high` - default `high`)

## Timeouts and limits (defaults)

- ALWAYSGREEN_MAX_ITERS (default 5)
- ALWAYSGREEN_RUN_TIMEOUT_SEC (default 300)
- ALWAYSGREEN_TEST_TIMEOUT_SEC (default 120)
- ALWAYSGREEN_LLM_TIMEOUT_SEC (default 60)
- ALWAYSGREEN_MIN_REPO_RUN_INTERVAL_SEC (default 600)
- ALWAYSGREEN_MAX_DAILY_LLM_CALLS (default 200)
- ALWAYSGREEN_WARN_DAILY_LLM_CALLS_PCT (default 0.8)

## Telemetry

- ALWAYSGREEN_ENABLE_TELEMETRY: `true` to save patches/reports (default false)
- ALWAYSGREEN_TELEMETRY_DIR: directory for run artifacts (default `telemetry`)

## Network allow-list

- ALWAYSGREEN_ALLOWED_DOMAINS: CSV or `["host"]` format; defaults include OpenAI, Anthropic, GitHub, PyPI.

## Example `.env`

```bash
OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=...
# ALWAYSGREEN_DEFAULT_LLM_MODEL=claude-3-5-sonnet
# ALWAYSGREEN_REASONING_EFFORT=medium  # Use 'low' or 'medium' for faster runs
ALWAYSGREEN_MAX_ITERS=5
ALWAYSGREEN_RUN_TIMEOUT_SEC=300
ALWAYSGREEN_TEST_TIMEOUT_SEC=120
ALWAYSGREEN_ENABLE_TELEMETRY=true
```

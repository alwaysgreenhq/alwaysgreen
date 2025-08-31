# AlwaysGreen — Quickstart Guide

## Installation

### Prerequisites
- Python 3.8+
- Git
- OpenAI or Anthropic API key

### Install AlwaysGreen
```bash
pip install -e .
```

## Configuration

### Option 1: Environment Variable
```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

### Option 2: .env File
Create a `.env` file in your project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
# Optional
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ALWAYSGREEN_MAX_ITERS=3
ALWAYSGREEN_RUN_TIMEOUT_SEC=600
```

## Running AlwaysGreen

### Basic Usage
```bash
alwaysgreen fix /path/to/repo
```

### With Options
```bash
alwaysgreen fix . --max-iters 3 --timeout 600
```

### Batch Evaluation
```bash
alwaysgreen eval --repos repos.yaml
```

## Inspecting Results

### View Artifacts
```bash
tree .alwaysgreen/<run>/
# Expected structure:
# .alwaysgreen/20250813T201234Z/
# ├── trace.jsonl       # Complete execution log
# ├── diffs/           # Patches for each iteration
# │   ├── step-1.patch
# │   └── step-2.patch
# └── reports/         # Test results
#     ├── step-1.xml
#     └── step-2.xml
```

### Check Test Results
```bash
# View the final test report
cat .alwaysgreen/<latest>/reports/final.xml
```

## Resetting After a Run

### Reset to Original State
```bash
git reset --hard HEAD
```

### Clean Working Directory
```bash
git clean -fd
```

## Troubleshooting

### Issue: API Key Not Found
**Solution:** Ensure your API key is set in environment or .env file

### Issue: Tests Still Failing After Max Iterations
**Solution:** Increase `--max-iters` or check if the failure is beyond automated fixing

### Issue: Timeout Reached
**Solution:** Increase `--timeout` value or optimize test suite

### Issue: Permission Denied
**Solution:** Ensure you have write permissions in the repository

## Getting Help

- Check logs: `.alwaysgreen/<run>/trace.jsonl`
- GitHub Issues: [github.com/alwaysgreen-ci/alwaysgreen/issues](https://github.com/alwaysgreen-ci/alwaysgreen/issues)
- Email support: support@alwaysgreen.ai

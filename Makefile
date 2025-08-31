SHELL := /bin/zsh
.PHONY: venv

# Set up a local Python virtual environment and install dependencies if available
venv:
	@echo "Creating .venv and installing dependencies (if any)"
	python3 -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip
	@if [ -f requirements.txt ]; then \
		. .venv/bin/activate && pip install -r requirements.txt; \
	fi
	@if [ -f demo-requirements.txt ]; then \
		. .venv/bin/activate && pip install -r demo-requirements.txt; \
	fi
	@if [ -f pyproject.toml ]; then \
		. .venv/bin/activate && pip install -e .; \
	fi

.PHONY: setup-demo smoke test-demo test-demo-verbose

# Run demo setup script to install AlwaysGreen demo into .venv
setup-demo:
	@bash scripts/setup_alwaysgreen.sh .venv

# Run Fly.io app smoke tests
smoke:
	@bash scripts/smoke_test.sh

# Run the AlwaysGreen CI-rescue demo test
test-demo:
	@bash scripts/test_alwaysgreen.sh

# Run the verbose AlwaysGreen CI-rescue demo test
test-demo-verbose:
	@bash scripts/test_alwaysgreen_verbose.sh

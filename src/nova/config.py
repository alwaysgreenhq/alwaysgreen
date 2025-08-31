from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field


def _default_allowed_domains() -> List[str]:
    return [
        "api.openai.com",
        "api.anthropic.com",
        "pypi.org",
        "files.pythonhosted.org",
        "github.com",
        "raw.githubusercontent.com",
    ]


def load_yaml_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from a YAML file."""
    try:
        import yaml

        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # Fallback if PyYAML is not available
        raise ImportError(
            "PyYAML is required for YAML config loading. Install with: pip install PyYAML"
        )


class AlwaysGreenSettings(BaseModel):
    """Runtime configuration for AlwaysGreen.

    Uses python-dotenv to load a local .env (if present), and reads values from
    environment variables. We avoid depending on pydantic-settings to keep
    compatibility consistent across Pydantic versions.
    """

    # Secrets and API endpoints
    openai_api_key: Optional[str] = Field(default=None)
    anthropic_api_key: Optional[str] = Field(default=None)
    openswe_base_url: Optional[str] = Field(default=None)
    openswe_api_key: Optional[str] = Field(default=None)

    # Policy and runtime settings
    allowed_domains: List[str] = Field(default_factory=_default_allowed_domains)
    max_iters: int = 5
    run_timeout_sec: int = 300
    test_timeout_sec: int = 120
    llm_call_timeout_sec: int = 60
    min_repo_run_interval_sec: int = 600
    max_daily_llm_calls: int = 200
    warn_daily_llm_calls_pct: float = 0.8
    telemetry_dir: str = "telemetry"
    enable_telemetry: bool = True  # Enable telemetry by default to save patches
    # Keep default consistent with from_env fallback:
    default_llm_model: str = "gpt-5"
    pr_llm_model: str = "gpt-4o"  # Faster model for PR generation
    reasoning_effort: str = "high"  # Reasoning effort for GPT models (low/medium/high)
    whole_file_mode: bool = True  # Use whole file replacement instead of patches

    @classmethod
    def from_env(cls) -> "AlwaysGreenSettings":
        """Load settings from .env and environment variables."""
        load_dotenv()

        def _get(name: str, default: Optional[str] = None) -> Optional[str]:
            return os.environ.get(name, default)

        def _get_int(name: str, default: int) -> int:
            val = os.environ.get(name)
            try:
                return int(val) if val is not None else default
            except Exception:
                return default

        # Optional override for domain allow-list via ALWAYSGREEN_ALLOWED_DOMAINS.
        # Accepts CSV ("a.com,b.com") or JSON-like with brackets.
        domains_env = os.environ.get("ALWAYSGREEN_ALLOWED_DOMAINS")
        if domains_env:
            raw = domains_env.strip()
            if raw.startswith("[") and raw.endswith("]"):
                # tolerate simple JSON lists without importing json
                raw = raw.strip("[]")
            allowed = [
                d.strip().strip('"').strip("'") for d in raw.split(",") if d.strip()
            ]
        else:
            allowed = _default_allowed_domains()

        return cls(
            openai_api_key=_get("OPENAI_API_KEY"),
            anthropic_api_key=_get("ANTHROPIC_API_KEY"),
            openswe_base_url=_get("OPENSWE_BASE_URL"),
            openswe_api_key=_get("OPENSWE_API_KEY"),
            allowed_domains=allowed,
            max_iters=_get_int("ALWAYSGREEN_MAX_ITERS", 5),
            run_timeout_sec=_get_int("ALWAYSGREEN_RUN_TIMEOUT_SEC", 300),
            test_timeout_sec=_get_int("ALWAYSGREEN_TEST_TIMEOUT_SEC", 120),
            llm_call_timeout_sec=_get_int("ALWAYSGREEN_LLM_TIMEOUT_SEC", 60),
            min_repo_run_interval_sec=_get_int("ALWAYSGREEN_MIN_REPO_RUN_INTERVAL_SEC", 600),
            max_daily_llm_calls=_get_int("ALWAYSGREEN_MAX_DAILY_LLM_CALLS", 200),
            warn_daily_llm_calls_pct=float(
                os.environ.get("ALWAYSGREEN_WARN_DAILY_LLM_CALLS_PCT", 0.8)
            ),
            telemetry_dir=os.environ.get("ALWAYSGREEN_TELEMETRY_DIR", "telemetry"),
            enable_telemetry=os.environ.get("ALWAYSGREEN_ENABLE_TELEMETRY", "false").lower()
            == "true",
            default_llm_model=os.environ.get("ALWAYSGREEN_DEFAULT_LLM_MODEL", "gpt-5"),
            pr_llm_model=os.environ.get("ALWAYSGREEN_PR_LLM_MODEL", "gpt-4o"),
            reasoning_effort=os.environ.get("ALWAYSGREEN_REASONING_EFFORT", "high"),
            whole_file_mode=os.environ.get("ALWAYSGREEN_WHOLE_FILE_MODE", "true").lower()
            == "true",
        )


_CACHED_SETTINGS: Optional[AlwaysGreenSettings] = None


def get_settings() -> AlwaysGreenSettings:
    """Return a cached AlwaysGreenSettings instance loaded from environment (.env)."""
    global _CACHED_SETTINGS
    if _CACHED_SETTINGS is None:
        _CACHED_SETTINGS = AlwaysGreenSettings.from_env()
    return _CACHED_SETTINGS


# --- Back-compat alias -------------------------------------------------------
# Some callers import a module variable named `settings`:
#     from nova.config import settings
# Provide that alias while still supporting the cached getter.
# This is initialized at import time; if you need to re-read env in tests,
# call `_reset_settings_cache()` and re-import or reassign.
settings: AlwaysGreenSettings = get_settings()


def _reset_settings_cache() -> None:
    """Test helper: clear cache and refresh module-level `settings`."""
    global _CACHED_SETTINGS, settings
    _CACHED_SETTINGS = None
    settings = get_settings()


__all__ = [
    "AlwaysGreenSettings",
    "get_settings",
    "settings",
    "_reset_settings_cache",
    "load_yaml_config",
]

settings: AlwaysGreenSettings = get_settings()


def _reset_settings_cache() -> None:
    """Test helper: clear cache and refresh module-level `settings`."""
    global _CACHED_SETTINGS, settings
    _CACHED_SETTINGS = None
    settings = get_settings()


__all__ = [
    "AlwaysGreenSettings",
    "get_settings",
    "settings",
    "_reset_settings_cache",
    "load_yaml_config",
]

settings: AlwaysGreenSettings = get_settings()


def _reset_settings_cache() -> None:
    """Test helper: clear cache and refresh module-level `settings`."""
    global _CACHED_SETTINGS, settings
    _CACHED_SETTINGS = None
    settings = get_settings()


__all__ = [
    "AlwaysGreenSettings",
    "get_settings",
    "settings",
    "_reset_settings_cache",
    "load_yaml_config",
]

settings: AlwaysGreenSettings = get_settings()


def _reset_settings_cache() -> None:
    """Test helper: clear cache and refresh module-level `settings`."""
    global _CACHED_SETTINGS, settings
    _CACHED_SETTINGS = None
    settings = get_settings()


__all__ = [
    "AlwaysGreenSettings",
    "get_settings",
    "settings",
    "_reset_settings_cache",
    "load_yaml_config",
]

settings: AlwaysGreenSettings = get_settings()


def _reset_settings_cache() -> None:
    """Test helper: clear cache and refresh module-level `settings`."""
    global _CACHED_SETTINGS, settings
    _CACHED_SETTINGS = None
    settings = get_settings()


__all__ = [
    "AlwaysGreenSettings",
    "get_settings",
    "settings",
    "_reset_settings_cache",
    "load_yaml_config",
]

settings: AlwaysGreenSettings = get_settings()


def _reset_settings_cache() -> None:
    """Test helper: clear cache and refresh module-level `settings`."""
    global _CACHED_SETTINGS, settings
    _CACHED_SETTINGS = None
    settings = get_settings()


__all__ = [
    "AlwaysGreenSettings",
    "get_settings",
    "settings",
    "_reset_settings_cache",
    "load_yaml_config",
]

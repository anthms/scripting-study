#!/usr/bin/env python3
"""DevOps Python: Environment variable handling and system health checks."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass, field


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str


@dataclass
class HealthReport:
    results: list[CheckResult] = field(default_factory=list)

    def add(self, result: CheckResult) -> None:
        self.results.append(result)

    @property
    def all_passed(self) -> bool:
        return all(r.passed for r in self.results)

    def print_summary(self) -> None:
        for r in self.results:
            icon = "✓" if r.passed else "✗"
            print(f"  {icon} {r.name:<30} {r.message}")
        print()
        status = "HEALTHY" if self.all_passed else "DEGRADED"
        print(f"  Status: {status}")


# ── Check functions ───────────────────────────────────────────────────────────

def check_required_env_vars(required: list[str]) -> list[CheckResult]:
    """Check that required environment variables are set."""
    results = []
    for var in required:
        value = os.environ.get(var)
        results.append(CheckResult(
            name=f"env:{var}",
            passed=bool(value),
            message=f"= {value!r}" if value else "NOT SET",
        ))
    return results


def check_required_tools(tools: list[str]) -> list[CheckResult]:
    """Check that required CLI tools are available on PATH."""
    results = []
    for tool in tools:
        path = shutil.which(tool)
        results.append(CheckResult(
            name=f"tool:{tool}",
            passed=bool(path),
            message=path or "not found",
        ))
    return results


def check_python_version(min_major: int = 3, min_minor: int = 8) -> CheckResult:
    """Check that Python version meets minimum requirement."""
    major, minor = sys.version_info[:2]
    passed = (major, minor) >= (min_major, min_minor)
    return CheckResult(
        name=f"python>={min_major}.{min_minor}",
        passed=passed,
        message=f"{major}.{minor}.{sys.version_info.micro}",
    )


def check_git_repo(path: str = ".") -> CheckResult:
    """Check that the current directory is inside a git repository."""
    result = subprocess.run(
        ["git", "-C", path, "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True,
    )
    passed = result.returncode == 0
    return CheckResult(
        name="git repo",
        passed=passed,
        message="yes" if passed else result.stderr.strip(),
    )


def get_system_info() -> dict[str, str]:
    """Return basic system information."""
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "python": sys.version.split()[0],
        "cwd": os.getcwd(),
    }


def get_env_config(prefix: str) -> dict[str, str]:
    """Return all environment variables starting with prefix (prefix stripped)."""
    return {
        k[len(prefix):]: v
        for k, v in os.environ.items()
        if k.startswith(prefix)
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    report = HealthReport()

    # Python version
    report.add(check_python_version(3, 8))

    # Required env vars
    for result in check_required_env_vars(["HOME", "PATH", "USER"]):
        report.add(result)

    # Required tools
    for result in check_required_tools(["git", "python3", "curl"]):
        report.add(result)

    # Git repo check
    report.add(check_git_repo())

    print("=== environment health check ===")
    report.print_summary()

    print("=== system info ===")
    for key, value in get_system_info().items():
        print(f"  {key:<12} : {value}")

    # Show any APP_ prefixed env vars (useful in CI/CD)
    app_vars = get_env_config("APP_")
    if app_vars:
        print("\n=== APP_ env vars ===")
        for k, v in sorted(app_vars.items()):
            print(f"  APP_{k:<15} = {v}")
    else:
        print("\n=== APP_ env vars ===")
        print("  (none set — export APP_NAME=myapp to test)")

    if not report.all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()

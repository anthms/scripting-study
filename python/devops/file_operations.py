#!/usr/bin/env python3
"""DevOps Python: File and directory operations common in CI/CD pipelines."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path


def create_project_tree(root: Path) -> None:
    """Create a sample project directory tree."""
    for d in ["logs", "config", "releases/v1.0", "releases/v1.1", "artifacts"]:
        (root / d).mkdir(parents=True, exist_ok=True)
    print("=== project tree ===")
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            rel = path.relative_to(root)
            depth = len(rel.parts) - 1
            print(f"  {'  ' * depth}{rel.parts[-1]}/")


def write_env_file(path: Path) -> None:
    """Write a .env style config file."""
    content = (
        "APP_NAME=my-service\n"
        "APP_PORT=8080\n"
        "APP_ENV=production\n"
        "LOG_LEVEL=info\n"
    )
    path.write_text(content)
    print(f"\n=== wrote {path.name} ===")
    print(path.read_text(), end="")


def parse_env_file(path: Path) -> dict[str, str]:
    """Parse a key=value .env file into a dict, ignoring blanks and comments."""
    result: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        result[key.strip()] = value.strip()
    return result


def atomic_write(path: Path, new_content: str) -> None:
    """Write a file atomically via a temp file + rename."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        tmp.write_text(new_content)
        tmp.replace(path)   # atomic on POSIX systems
    except Exception:
        tmp.unlink(missing_ok=True)
        raise


def write_json_report(path: Path, data: dict) -> None:
    """Write a JSON report file with pretty formatting."""
    path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"\n=== JSON report ({path.name}) ===")
    print(path.read_text(), end="")


def find_logs(root: Path, pattern: str = "*.log") -> list[Path]:
    """Return sorted list of log files matching pattern."""
    return sorted(root.rglob(pattern))


def rotate_logs(log_dir: Path, keep: int = 3) -> int:
    """Delete old log files, keeping only the <keep> most recent. Returns deleted count."""
    logs = sorted(log_dir.glob("*.log"), key=lambda p: p.stat().st_mtime)
    to_delete = logs[: max(0, len(logs) - keep)]
    for f in to_delete:
        f.unlink()
    return len(to_delete)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        # Directory tree
        create_project_tree(root)

        # .env file
        env_file = root / "config" / "app.env"
        write_env_file(env_file)

        # Parse env
        print("\n=== parsed env ===")
        parsed = parse_env_file(env_file)
        for k, v in parsed.items():
            print(f"  {k:<12} = {v}")

        # Atomic write
        original = env_file.read_text()
        atomic_write(env_file, original + "UPDATED=true\n")
        print(f"\n=== after atomic write ===")
        print(f"  last line: {env_file.read_text().splitlines()[-1]}")

        # JSON report
        report = {
            "pipeline": "release-1.0",
            "stages": ["build", "test", "deploy"],
            "status": "success",
            "duration_seconds": 142,
        }
        write_json_report(root / "artifacts" / "report.json", report)

        # Log rotation
        log_dir = root / "logs"
        for i in range(5):
            (log_dir / f"app-2024-01-0{i + 1}.log").write_text(f"log {i}\n")
        deleted = rotate_logs(log_dir, keep=3)
        remaining = find_logs(log_dir)
        print(f"\n=== log rotation ===")
        print(f"  deleted {deleted} old logs, {len(remaining)} remaining:")
        for f in remaining:
            print(f"  - {f.name}")


if __name__ == "__main__":
    main()

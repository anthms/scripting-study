"""Tests for python/devops/file_operations.py"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from devops.file_operations import (
    atomic_write,
    create_project_tree,
    find_logs,
    parse_env_file,
    rotate_logs,
    write_env_file,
    write_json_report,
)


@pytest.fixture()
def tmp(tmp_path: Path) -> Path:
    return tmp_path


class TestCreateProjectTree:
    def test_creates_expected_directories(self, tmp: Path) -> None:
        create_project_tree(tmp)
        assert (tmp / "logs").is_dir()
        assert (tmp / "config").is_dir()
        assert (tmp / "releases" / "v1.0").is_dir()
        assert (tmp / "releases" / "v1.1").is_dir()
        assert (tmp / "artifacts").is_dir()

    def test_idempotent(self, tmp: Path) -> None:
        create_project_tree(tmp)
        create_project_tree(tmp)  # should not raise


class TestEnvFile:
    def test_write_creates_file(self, tmp: Path) -> None:
        env_file = tmp / "app.env"
        write_env_file(env_file)
        assert env_file.exists()

    def test_write_contains_expected_keys(self, tmp: Path) -> None:
        env_file = tmp / "app.env"
        write_env_file(env_file)
        content = env_file.read_text()
        assert "APP_NAME" in content
        assert "APP_PORT" in content

    def test_parse_returns_dict(self, tmp: Path) -> None:
        env_file = tmp / "app.env"
        write_env_file(env_file)
        parsed = parse_env_file(env_file)
        assert isinstance(parsed, dict)
        assert parsed["APP_NAME"] == "my-service"
        assert parsed["APP_PORT"] == "8080"

    def test_parse_ignores_blank_lines(self, tmp: Path) -> None:
        env_file = tmp / "test.env"
        env_file.write_text("\n# comment\nKEY=value\n\n")
        parsed = parse_env_file(env_file)
        assert parsed == {"KEY": "value"}

    def test_parse_ignores_comments(self, tmp: Path) -> None:
        env_file = tmp / "test.env"
        env_file.write_text("# this is a comment\nKEY=val\n")
        parsed = parse_env_file(env_file)
        assert "# this is a comment" not in parsed
        assert parsed["KEY"] == "val"


class TestAtomicWrite:
    def test_content_is_written(self, tmp: Path) -> None:
        target = tmp / "output.txt"
        atomic_write(target, "hello\n")
        assert target.read_text() == "hello\n"

    def test_overwrites_existing(self, tmp: Path) -> None:
        target = tmp / "output.txt"
        target.write_text("old content\n")
        atomic_write(target, "new content\n")
        assert target.read_text() == "new content\n"

    def test_no_leftover_tmp_file(self, tmp: Path) -> None:
        target = tmp / "output.txt"
        atomic_write(target, "data\n")
        tmp_files = list(tmp.glob("*.tmp"))
        assert tmp_files == [], f"Unexpected tmp files: {tmp_files}"


class TestJsonReport:
    def test_creates_valid_json(self, tmp: Path) -> None:
        report_file = tmp / "report.json"
        data = {"status": "ok", "count": 3}
        write_json_report(report_file, data)
        loaded = json.loads(report_file.read_text())
        assert loaded == data

    def test_pretty_formatted(self, tmp: Path) -> None:
        report_file = tmp / "report.json"
        write_json_report(report_file, {"a": 1})
        # pretty JSON has newlines
        assert "\n" in report_file.read_text()


class TestFindLogs:
    def test_finds_log_files(self, tmp: Path) -> None:
        for i in range(3):
            (tmp / f"app-{i}.log").write_text(f"log {i}\n")
        logs = find_logs(tmp)
        assert len(logs) == 3

    def test_returns_sorted_list(self, tmp: Path) -> None:
        for name in ["c.log", "a.log", "b.log"]:
            (tmp / name).write_text("")
        logs = find_logs(tmp)
        names = [f.name for f in logs]
        assert names == sorted(names)

    def test_no_logs_returns_empty(self, tmp: Path) -> None:
        assert find_logs(tmp) == []


class TestRotateLogs:
    def test_keeps_most_recent(self, tmp: Path) -> None:
        for i in range(5):
            (tmp / f"app-{i}.log").write_text(f"log {i}\n")
        deleted = rotate_logs(tmp, keep=3)
        assert deleted == 2
        assert len(list(tmp.glob("*.log"))) == 3

    def test_does_not_delete_when_under_limit(self, tmp: Path) -> None:
        for i in range(2):
            (tmp / f"app-{i}.log").write_text("")
        deleted = rotate_logs(tmp, keep=5)
        assert deleted == 0

    def test_empty_dir(self, tmp: Path) -> None:
        deleted = rotate_logs(tmp, keep=3)
        assert deleted == 0

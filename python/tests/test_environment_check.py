"""Tests for python/devops/environment_check.py"""

from __future__ import annotations

import os
import sys

import pytest

from devops.environment_check import (
    CheckResult,
    HealthReport,
    check_python_version,
    check_required_env_vars,
    check_required_tools,
    get_env_config,
    get_system_info,
)


class TestCheckResult:
    def test_passed_true(self) -> None:
        r = CheckResult(name="test", passed=True, message="ok")
        assert r.passed is True

    def test_passed_false(self) -> None:
        r = CheckResult(name="test", passed=False, message="fail")
        assert r.passed is False


class TestHealthReport:
    def test_all_passed_when_empty(self) -> None:
        report = HealthReport()
        assert report.all_passed is True

    def test_all_passed_when_all_true(self) -> None:
        report = HealthReport()
        report.add(CheckResult("a", True, "ok"))
        report.add(CheckResult("b", True, "ok"))
        assert report.all_passed is True

    def test_not_all_passed_when_one_fails(self) -> None:
        report = HealthReport()
        report.add(CheckResult("a", True, "ok"))
        report.add(CheckResult("b", False, "fail"))
        assert report.all_passed is False

    def test_add_accumulates_results(self) -> None:
        report = HealthReport()
        report.add(CheckResult("x", True, "ok"))
        report.add(CheckResult("y", True, "ok"))
        assert len(report.results) == 2


class TestCheckRequiredEnvVars:
    def test_set_variable_passes(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MY_TEST_VAR", "hello")
        results = check_required_env_vars(["MY_TEST_VAR"])
        assert results[0].passed is True

    def test_unset_variable_fails(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DEFINITELY_NOT_SET_XYZ", raising=False)
        results = check_required_env_vars(["DEFINITELY_NOT_SET_XYZ"])
        assert results[0].passed is False

    def test_returns_one_result_per_var(self) -> None:
        results = check_required_env_vars(["HOME", "PATH"])
        assert len(results) == 2

    def test_result_names_match_vars(self) -> None:
        results = check_required_env_vars(["HOME"])
        assert results[0].name == "env:HOME"


class TestCheckRequiredTools:
    def test_existing_tool_passes(self) -> None:
        # python3 / python should always exist in the test environment
        tool = "python3" if sys.platform != "win32" else "python"
        results = check_required_tools([tool])
        assert results[0].passed is True

    def test_nonexistent_tool_fails(self) -> None:
        results = check_required_tools(["__tool_that_does_not_exist_xyzzy__"])
        assert results[0].passed is False

    def test_result_name_prefixed(self) -> None:
        results = check_required_tools(["git"])
        assert results[0].name.startswith("tool:")


class TestCheckPythonVersion:
    def test_current_version_passes(self) -> None:
        major, minor = sys.version_info[:2]
        result = check_python_version(major, minor)
        assert result.passed is True

    def test_higher_requirement_fails(self) -> None:
        result = check_python_version(99, 0)
        assert result.passed is False

    def test_message_contains_version(self) -> None:
        result = check_python_version(3, 8)
        assert "." in result.message


class TestGetSystemInfo:
    def test_returns_expected_keys(self) -> None:
        info = get_system_info()
        for key in ("os", "os_version", "machine", "python", "cwd"):
            assert key in info, f"Missing key: {key}"

    def test_all_values_are_strings(self) -> None:
        info = get_system_info()
        for k, v in info.items():
            assert isinstance(v, str), f"Expected str for {k}, got {type(v)}"


class TestGetEnvConfig:
    def test_returns_matching_vars(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MYAPP_HOST", "localhost")
        monkeypatch.setenv("MYAPP_PORT", "8080")
        monkeypatch.setenv("OTHER_VAR", "ignored")
        result = get_env_config("MYAPP_")
        assert result == {"HOST": "localhost", "PORT": "8080"}

    def test_empty_when_no_matches(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Ensure no XYZZY_ vars exist
        for k in list(os.environ):
            if k.startswith("XYZZY_"):
                monkeypatch.delenv(k)
        result = get_env_config("XYZZY_")
        assert result == {}

    def test_prefix_stripped_from_keys(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("PREFIX_KEY", "value")
        result = get_env_config("PREFIX_")
        assert "KEY" in result
        assert "PREFIX_KEY" not in result

#!/usr/bin/env bash
# Bash test runner — lightweight assertions without external dependencies
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BASH_DIR="$REPO_ROOT/bash"

# ── Test framework ────────────────────────────────────────────────────────────

PASS=0
FAIL=0
ERRORS=()

assert_exit_ok() {
    local desc="$1"
    shift
    if "$@" &>/dev/null; then
        echo "  PASS: $desc"
        PASS=$(( PASS + 1 ))
    else
        echo "  FAIL: $desc"
        ERRORS+=("$desc")
        FAIL=$(( FAIL + 1 ))
    fi
}

assert_output_contains() {
    local desc="$1"
    local expected="$2"
    shift 2
    local output
    output=$("$@" 2>&1)
    if echo "$output" | grep -qF "$expected"; then
        echo "  PASS: $desc"
        PASS=$(( PASS + 1 ))
    else
        echo "  FAIL: $desc"
        echo "        expected output to contain: '$expected'"
        echo "        actual output: $output"
        ERRORS+=("$desc")
        FAIL=$(( FAIL + 1 ))
    fi
}

# ── Basics: variables.sh ──────────────────────────────────────────────────────

echo "=== variables.sh ==="
assert_exit_ok       "exits successfully"             bash "$BASH_DIR/basics/variables.sh"
assert_output_contains "prints first 5 chars"  "Hello"   bash "$BASH_DIR/basics/variables.sh"
assert_output_contains "uppercase works"       "HELLO"   bash "$BASH_DIR/basics/variables.sh"
assert_output_contains "array element"         "banana"  bash "$BASH_DIR/basics/variables.sh"
assert_output_contains "associative array"     "localhost" bash "$BASH_DIR/basics/variables.sh"

# ── Basics: loops.sh ─────────────────────────────────────────────────────────

echo ""
echo "=== loops.sh ==="
assert_exit_ok       "exits successfully"              bash "$BASH_DIR/basics/loops.sh"
assert_output_contains "C-style loop output" "i = 3"   bash "$BASH_DIR/basics/loops.sh"
assert_output_contains "for-in service"      "redis"   bash "$BASH_DIR/basics/loops.sh"
assert_output_contains "while loop output"   "attempt 2 of 3" bash "$BASH_DIR/basics/loops.sh"
assert_output_contains "break skips even"    "odd: 7"  bash "$BASH_DIR/basics/loops.sh"
assert_output_contains "mapfile words"       "two"     bash "$BASH_DIR/basics/loops.sh"

# ── Basics: functions.sh ──────────────────────────────────────────────────────

echo ""
echo "=== functions.sh ==="
assert_exit_ok       "exits successfully"               bash "$BASH_DIR/basics/functions.sh"
assert_output_contains "default arg"        "Hello, World" bash "$BASH_DIR/basics/functions.sh"
assert_output_contains "named arg"          "Hello, DevOps" bash "$BASH_DIR/basics/functions.sh"
assert_output_contains "to_upper"           "Uppercase: HELLO" bash "$BASH_DIR/basics/functions.sh"
assert_output_contains "is_even detects"    "4 is even"    bash "$BASH_DIR/basics/functions.sh"
assert_output_contains "sum variadic"       "Sum 1 2 3 4 5 = 15" bash "$BASH_DIR/basics/functions.sh"
assert_output_contains "factorial"          "5! = 120"     bash "$BASH_DIR/basics/functions.sh"
assert_output_contains "nameref array"      "automation"   bash "$BASH_DIR/basics/functions.sh"

# ── DevOps: file_operations.sh ───────────────────────────────────────────────

echo ""
echo "=== file_operations.sh ==="
assert_exit_ok       "exits successfully"               bash "$BASH_DIR/devops/file_operations.sh"
assert_output_contains "creates logs dir"   "/logs"        bash "$BASH_DIR/devops/file_operations.sh"
assert_output_contains "reads APP_NAME"     "APP_NAME"     bash "$BASH_DIR/devops/file_operations.sh"
assert_output_contains "atomic write"       "Atomic update complete" bash "$BASH_DIR/devops/file_operations.sh"
assert_output_contains "finds log files"    "app-2024"     bash "$BASH_DIR/devops/file_operations.sh"
assert_output_contains "disk check runs"    "threshold"    bash "$BASH_DIR/devops/file_operations.sh"

# ── DevOps: environment_check.sh ─────────────────────────────────────────────

echo ""
echo "=== environment_check.sh ==="
assert_exit_ok       "exits successfully"               bash "$BASH_DIR/devops/environment_check.sh"
assert_output_contains "detects bash"       "Bash"         bash "$BASH_DIR/devops/environment_check.sh"
assert_output_contains "finds HOME var"     "HOME"         bash "$BASH_DIR/devops/environment_check.sh"
assert_output_contains "reports CPUs"       "CPUs"         bash "$BASH_DIR/devops/environment_check.sh"

# ── Summary ───────────────────────────────────────────────────────────────────

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: $PASS passed, $FAIL failed"

if (( FAIL > 0 )); then
    echo "Failed tests:"
    for err in "${ERRORS[@]}"; do
        echo "  - $err"
    done
    exit 1
fi

echo "All tests passed!"

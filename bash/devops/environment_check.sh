#!/usr/bin/env bash
# DevOps Bash: Environment and system health checks
set -euo pipefail

# ── Required tools check ──────────────────────────────────────────────────────

echo "=== required tools ==="
REQUIRED_TOOLS=("git" "curl" "python3" "awk" "sed")
missing=()

for tool in "${REQUIRED_TOOLS[@]}"; do
    if command -v "$tool" &>/dev/null; then
        printf "  %-10s ✓ (%s)\n" "$tool" "$(command -v "$tool")"
    else
        printf "  %-10s ✗ NOT FOUND\n" "$tool"
        missing+=("$tool")
    fi
done

if (( ${#missing[@]} > 0 )); then
    echo "WARNING: Missing tools: ${missing[*]}" >&2
fi

# ── OS detection ──────────────────────────────────────────────────────────────

echo ""
echo "=== OS detection ==="
detect_os() {
    if [[ -f /etc/os-release ]]; then
        # shellcheck source=/dev/null
        . /etc/os-release
        echo "$NAME $VERSION_ID"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS $(sw_vers -productVersion)"
    else
        echo "Unknown OS"
    fi
}
echo "  OS: $(detect_os)"
echo "  Kernel: $(uname -r)"
echo "  Arch: $(uname -m)"

# ── Environment variable validation ───────────────────────────────────────────

echo ""
echo "=== environment variables ==="

# List of required env vars with descriptions
declare -A REQUIRED_VARS
REQUIRED_VARS["HOME"]="user home directory"
REQUIRED_VARS["PATH"]="executable search path"
REQUIRED_VARS["USER"]="current username"

all_set=true
for var in "${!REQUIRED_VARS[@]}"; do
    if [[ -n "${!var:-}" ]]; then
        printf "  %-8s ✓  ${REQUIRED_VARS[$var]}\n" "$var"
    else
        printf "  %-8s ✗  ${REQUIRED_VARS[$var]} — NOT SET\n" "$var"
        all_set=false
    fi
done
$all_set && echo "  All required vars are set."

# ── CPU and memory snapshot ────────────────────────────────────────────────────

echo ""
echo "=== system resources ==="

# CPU count
cpu_count=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "unknown")
echo "  CPUs        : $cpu_count"

# Memory (Linux)
if [[ -f /proc/meminfo ]]; then
    mem_total=$(awk '/MemTotal/ {printf "%.0f MiB", $2/1024}' /proc/meminfo)
    mem_avail=$(awk '/MemAvailable/ {printf "%.0f MiB", $2/1024}' /proc/meminfo)
    echo "  Memory total: $mem_total"
    echo "  Memory avail: $mem_avail"
fi

# ── Network connectivity ──────────────────────────────────────────────────────

echo ""
echo "=== network check ==="
check_host() {
    local host="$1"
    if curl -sf --max-time 3 "https://$host" -o /dev/null 2>/dev/null; then
        echo "  $host ✓ reachable"
    else
        echo "  $host ✗ unreachable (or timeout)"
    fi
}

check_host "github.com"
check_host "pypi.org"

# ── Bash version check ────────────────────────────────────────────────────────

echo ""
echo "=== bash version ==="
major="${BASH_VERSINFO[0]}"
minor="${BASH_VERSINFO[1]}"
echo "  Bash ${major}.${minor}"
if (( major < 4 )); then
    echo "  WARNING: Bash 4+ recommended (associative arrays, nameref, etc.)"
else
    echo "  OK: Bash 4+ features available"
fi

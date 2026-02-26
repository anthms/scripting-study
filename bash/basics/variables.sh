#!/usr/bin/env bash
# Intermediate Bash: Variables, parameter expansion, and scoping
set -euo pipefail

# ── String manipulation ───────────────────────────────────────────────────────

greeting="Hello, World"

# Substring: ${var:offset:length}
echo "First 5 chars : ${greeting:0:5}"

# Length
echo "Length         : ${#greeting}"

# Replace first match
echo "Replace first  : ${greeting/l/L}"

# Replace all matches
echo "Replace all    : ${greeting//l/L}"

# Uppercase / lowercase (Bash 4+)
echo "Uppercase      : ${greeting^^}"
echo "Lowercase      : ${greeting,,}"

# ── Default values ────────────────────────────────────────────────────────────

# ${var:-default}  → use default if var is unset or empty
unset MY_VAR
echo "Default        : ${MY_VAR:-'not set'}"

# ${var:=default}  → assign default if var is unset or empty
echo "Assign default : ${MY_VAR:='assigned now'}"
echo "MY_VAR is now  : $MY_VAR"

# ${var:?message}  → exit with error if var is unset or empty (comment out to test)
# echo "${REQUIRED_VAR:?'REQUIRED_VAR must be set'}"

# ── Arrays ────────────────────────────────────────────────────────────────────

fruits=("apple" "banana" "cherry")

echo ""
echo "All elements   : ${fruits[*]}"
echo "Element [1]    : ${fruits[1]}"
echo "Array length   : ${#fruits[@]}"

# Slice: elements 1 and 2
echo "Slice [1..2]   : ${fruits[@]:1:2}"

# Append
fruits+=("date")
echo "After append   : ${fruits[*]}"

# ── Associative arrays (Bash 4+) ──────────────────────────────────────────────

declare -A config
config["host"]="localhost"
config["port"]="8080"
config["env"]="development"

echo ""
echo "Config host    : ${config[host]}"
echo "Config keys    : ${!config[@]}"
echo "Config values  : ${config[@]}"

# ── Arithmetic ────────────────────────────────────────────────────────────────

count=5
((count++))
echo ""
echo "After count++  : $count"
echo "count * 3      : $((count * 3))"
echo "count % 4      : $((count % 4))"

# ── Readonly & export ─────────────────────────────────────────────────────────

readonly MAX_RETRIES=3
export APP_ENV="production"
echo ""
echo "MAX_RETRIES    : $MAX_RETRIES"
echo "APP_ENV        : $APP_ENV"

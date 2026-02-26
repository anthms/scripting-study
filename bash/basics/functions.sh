#!/usr/bin/env bash
# Intermediate Bash: Functions, arguments, return values, and scope
set -euo pipefail

# ── Basic function ────────────────────────────────────────────────────────────

greet() {
    local name="${1:-World}"   # positional arg with default
    echo "Hello, ${name}!"
}

greet
greet "DevOps"

# ── Return values via stdout ──────────────────────────────────────────────────

to_upper() {
    echo "${1^^}"
}

result=$(to_upper "hello")
echo "Uppercase: $result"

# ── Return codes ──────────────────────────────────────────────────────────────

is_even() {
    (( $1 % 2 == 0 ))   # returns 0 (true) if even, 1 (false) if odd
}

for n in 3 4 7 8; do
    if is_even "$n"; then
        echo "$n is even"
    else
        echo "$n is odd"
    fi
done

# ── Variadic functions ($@ and $*) ────────────────────────────────────────────

echo ""
echo "=== variadic ==="

sum_all() {
    local total=0
    for num in "$@"; do
        ((total += num))
    done
    echo "$total"
}

echo "Sum 1 2 3 4 5 = $(sum_all 1 2 3 4 5)"

# ── Local vs global scope ─────────────────────────────────────────────────────

echo ""
echo "=== scope ==="

GLOBAL_VAR="I am global"

demonstrate_scope() {
    local local_var="I am local"
    GLOBAL_VAR="modified by function"
    echo "Inside  local_var : $local_var"
    echo "Inside  GLOBAL_VAR: $GLOBAL_VAR"
}

demonstrate_scope
echo "Outside GLOBAL_VAR: $GLOBAL_VAR"
# local_var is not accessible here

# ── Recursive function ────────────────────────────────────────────────────────

echo ""
echo "=== recursion ==="

factorial() {
    local n=$1
    if [[ $n -le 1 ]]; then
        echo 1
    else
        local sub
        sub=$(factorial $((n - 1)))
        echo $((n * sub))
    fi
}

echo "5! = $(factorial 5)"

# ── Function as error handler ─────────────────────────────────────────────────

echo ""
echo "=== error handling ==="

die() {
    local msg="${1:-An error occurred}"
    local code="${2:-1}"
    echo "ERROR: $msg" >&2
    exit "$code"
}

safe_divide() {
    local a=$1 b=$2
    if [[ $b -eq 0 ]]; then
        die "Division by zero" 1
    fi
    echo $((a / b))
}

echo "10 / 2 = $(safe_divide 10 2)"
# Uncommenting below would exit with an error:
# safe_divide 5 0

# ── Passing arrays to functions (via nameref, Bash 4.3+) ─────────────────────

echo ""
echo "=== nameref array param ==="

print_array() {
    local -n arr_ref=$1   # nameref to the caller's array
    for item in "${arr_ref[@]}"; do
        echo "  - $item"
    done
}

my_list=("ci" "cd" "devops" "automation")
print_array my_list

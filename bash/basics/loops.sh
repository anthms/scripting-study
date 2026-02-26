#!/usr/bin/env bash
# Intermediate Bash: Loops and iteration patterns
set -euo pipefail

# ── C-style for loop ──────────────────────────────────────────────────────────

echo "=== C-style for loop ==="
for ((i = 1; i <= 5; i++)); do
    printf "  i = %d\n" "$i"
done

# ── for-in over an array ──────────────────────────────────────────────────────

echo ""
echo "=== for-in array ==="
services=("nginx" "postgres" "redis" "app")
for svc in "${services[@]}"; do
    printf "  service: %s\n" "$svc"
done

# ── Brace expansion range ─────────────────────────────────────────────────────

echo ""
echo "=== brace expansion (01..05) ==="
for n in {01..05}; do
    printf "  item_%s\n" "$n"
done

# ── while loop with counter ───────────────────────────────────────────────────

echo ""
echo "=== while loop ==="
attempt=1
max=3
while [[ $attempt -le $max ]]; do
    printf "  attempt %d of %d\n" "$attempt" "$max"
    ((attempt++))
done

# ── until loop ────────────────────────────────────────────────────────────────

echo ""
echo "=== until loop ==="
count=0
until [[ $count -ge 3 ]]; do
    printf "  count = %d\n" "$count"
    (( ++count ))
done

# ── Loop with break / continue ────────────────────────────────────────────────

echo ""
echo "=== break and continue ==="
for i in {1..10}; do
    if [[ $((i % 2)) -eq 0 ]]; then
        continue  # skip even numbers
    fi
    if [[ $i -gt 7 ]]; then
        break     # stop after 7
    fi
    printf "  odd: %d\n" "$i"
done

# ── Reading lines from a file / process substitution ─────────────────────────

echo ""
echo "=== process substitution (read lines) ==="
while IFS= read -r line; do
    printf "  line: %s\n" "$line"
done < <(printf "alpha\nbeta\ngamma\n")

# ── Iterating over command output with mapfile ────────────────────────────────

echo ""
echo "=== mapfile (readarray) ==="
mapfile -t words < <(printf "one\ntwo\nthree\n")
for word in "${words[@]}"; do
    printf "  word: %s\n" "$word"
done

# ── Nested loops with labels (using functions) ────────────────────────────────

echo ""
echo "=== nested loops ==="
for row in 1 2 3; do
    for col in A B C; do
        printf "  (%d,%s)" "$row" "$col"
    done
    echo ""
done

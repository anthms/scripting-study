#!/usr/bin/env bash
# DevOps Bash: Common file and directory operations
set -euo pipefail

WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT

echo "Working in: $WORK_DIR"

# ── Create structured directories ─────────────────────────────────────────────

mkdir -p "$WORK_DIR"/{logs,config,releases/v1.0,releases/v1.1}
echo "Created directory tree"
find "$WORK_DIR" -type d | sort | sed "s|$WORK_DIR||"

# ── Write files ───────────────────────────────────────────────────────────────

echo ""
# Write with heredoc
cat > "$WORK_DIR/config/app.env" <<EOF
APP_NAME=my-service
APP_PORT=8080
APP_ENV=production
LOG_LEVEL=info
EOF

# Append a line
echo "DEPLOY_DATE=$(date +%Y-%m-%d)" >> "$WORK_DIR/config/app.env"

echo "=== app.env ==="
cat "$WORK_DIR/config/app.env"

# ── Read and parse key=value files ───────────────────────────────────────────

echo ""
echo "=== parsing key=value ==="
while IFS='=' read -r key value; do
    # Skip blank lines and comments
    [[ -z "$key" || "$key" == \#* ]] && continue
    printf "  %-15s → %s\n" "$key" "$value"
done < "$WORK_DIR/config/app.env"

# ── Safe file replacement (atomic write) ─────────────────────────────────────

echo ""
echo "=== atomic write ==="
target="$WORK_DIR/config/app.env"
tmp_file=$(mktemp "$target.XXXXXX")
# Write to temp then move — safe against partial writes
cp "$target" "$tmp_file"
echo "UPDATED=true" >> "$tmp_file"
mv "$tmp_file" "$target"
echo "Atomic update complete. New last line: $(tail -1 "$target")"

# ── Backup with timestamp ─────────────────────────────────────────────────────

echo ""
echo "=== backup ==="
backup() {
    local src="$1"
    local dest="${src}.bak.$(date +%Y%m%dT%H%M%S)"
    cp "$src" "$dest"
    echo "Backed up to: $(basename "$dest")"
}
backup "$WORK_DIR/config/app.env"

# ── Find files by pattern and age ─────────────────────────────────────────────

echo ""
echo "=== find by pattern ==="
touch "$WORK_DIR/logs/app-2024-01-01.log"
touch "$WORK_DIR/logs/app-2024-01-02.log"
touch "$WORK_DIR/logs/app-2024-01-03.log"

echo "Log files found:"
find "$WORK_DIR/logs" -name "*.log" | sort | while read -r f; do
    echo "  $(basename "$f")"
done

# ── Count lines / words in a file ────────────────────────────────────────────

echo ""
echo "=== file stats ==="
wc_out=$(wc -l < "$WORK_DIR/config/app.env")
echo "Lines in app.env: $wc_out"

# ── Check disk space and alert if above threshold ────────────────────────────

echo ""
echo "=== disk space check ==="
check_disk() {
    local path="${1:-/}"
    local threshold="${2:-90}"
    local usage
    usage=$(df -h "$path" | awk 'NR==2 {gsub(/%/,"",$5); print $5}')
    if (( usage >= threshold )); then
        echo "WARNING: $path is at ${usage}% — above threshold of ${threshold}%" >&2
        return 1
    else
        echo "OK: $path is at ${usage}% (threshold: ${threshold}%)"
    fi
}
check_disk "/" 95

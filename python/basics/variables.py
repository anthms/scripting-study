#!/usr/bin/env python3
"""Intermediate Python: Variables, type hints, data types, and string operations."""

from __future__ import annotations

# ── Type annotations ──────────────────────────────────────────────────────────

name: str = "DevOps Engineer"
port: int = 8080
ratio: float = 0.75
active: bool = True

print("=== scalar types ===")
print(f"  name   : {name!r}  ({type(name).__name__})")
print(f"  port   : {port}  ({type(port).__name__})")
print(f"  ratio  : {ratio}  ({type(ratio).__name__})")
print(f"  active : {active}  ({type(active).__name__})")

# ── String operations ─────────────────────────────────────────────────────────

print("\n=== string operations ===")
sentence = "  Hello, CI/CD World!  "
print(f"  strip       : {sentence.strip()!r}")
print(f"  upper       : {sentence.strip().upper()!r}")
print(f"  replace     : {sentence.replace('World', 'Pipeline')!r}")
print(f"  split       : {sentence.strip().split()}")
print(f"  startswith  : {sentence.strip().startswith('Hello')}")

# f-string formatting
version = "1.4.2"
build_id = 42
label = f"release-v{version}-build{build_id:04d}"
print(f"  label       : {label}")

# ── Collections ───────────────────────────────────────────────────────────────

print("\n=== list ===")
services: list[str] = ["nginx", "postgres", "redis"]
services.append("app")
print(f"  services    : {services}")
print(f"  first       : {services[0]}")
print(f"  slice [1:]  : {services[1:]}")
print(f"  length      : {len(services)}")

print("\n=== tuple (immutable) ===")
coordinates: tuple[int, int] = (42, 7)
x, y = coordinates   # unpacking
print(f"  x={x}, y={y}")

print("\n=== set ===")
tags: set[str] = {"ci", "cd", "devops", "ci"}   # duplicate dropped
tags.add("automation")
print(f"  tags  : {sorted(tags)}")

print("\n=== dict ===")
config: dict[str, str | int] = {
    "host": "localhost",
    "port": 5432,
    "dbname": "mydb",
}
config["user"] = "admin"
print(f"  host  : {config['host']}")
print(f"  keys  : {list(config.keys())}")
print(f"  items : {list(config.items())}")

# ── Default/fallback with dict.get ────────────────────────────────────────────

print("\n=== dict.get defaults ===")
timeout = config.get("timeout", 30)
print(f"  timeout (default 30) : {timeout}")

# ── Walrus operator (Python 3.8+) ─────────────────────────────────────────────

print("\n=== walrus operator ===")
data = [1, 5, 3, 8, 2, 9, 4]
if (n := len(data)) > 5:
    print(f"  List has {n} elements — processing in bulk")

# ── Unpacking / spread ────────────────────────────────────────────────────────

print("\n=== unpacking ===")
first, *middle, last = [10, 20, 30, 40, 50]
print(f"  first={first}, middle={middle}, last={last}")

# ── Type checking at runtime ──────────────────────────────────────────────────

print("\n=== isinstance checks ===")
for value in [42, "hello", 3.14, True, [1, 2]]:
    print(f"  {value!r:<15} → {type(value).__name__}")

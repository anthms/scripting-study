#!/usr/bin/env python3
"""Intermediate Python: Loops, comprehensions, generators, and iteration patterns."""

from __future__ import annotations

import itertools

# ── List comprehension ────────────────────────────────────────────────────────

print("=== list comprehension ===")
squares = [x ** 2 for x in range(1, 6)]
print(f"  squares     : {squares}")

evens = [x for x in range(10) if x % 2 == 0]
print(f"  evens       : {evens}")

# Nested comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [n for row in matrix for n in row]
print(f"  flat matrix : {flat}")

# ── Dict and set comprehensions ───────────────────────────────────────────────

print("\n=== dict / set comprehension ===")
services = ["nginx", "postgres", "redis", "app"]
service_map = {svc: len(svc) for svc in services}
print(f"  service_map : {service_map}")

unique_lengths = {len(svc) for svc in services}
print(f"  lengths set : {sorted(unique_lengths)}")

# ── Generator expression ──────────────────────────────────────────────────────

print("\n=== generator expression ===")
gen = (x ** 2 for x in range(100_000))   # memory-efficient
total = sum(gen)
print(f"  sum of squares (0..99999) : {total}")

# ── enumerate ─────────────────────────────────────────────────────────────────

print("\n=== enumerate ===")
stages = ["build", "test", "deploy"]
for idx, stage in enumerate(stages, start=1):
    print(f"  step {idx}: {stage}")

# ── zip ───────────────────────────────────────────────────────────────────────

print("\n=== zip ===")
hosts = ["web-01", "web-02", "db-01"]
ips   = ["10.0.0.1", "10.0.0.2", "10.0.1.1"]
for host, ip in zip(hosts, ips):
    print(f"  {host:<8} → {ip}")

# ── zip_longest ───────────────────────────────────────────────────────────────

print("\n=== zip_longest ===")
keys   = ["a", "b", "c"]
values = [1, 2]
for k, v in itertools.zip_longest(keys, values, fillvalue="N/A"):
    print(f"  {k} = {v}")

# ── while with sentinel ───────────────────────────────────────────────────────

print("\n=== while sentinel ===")
items = iter(["alpha", "beta", "STOP", "gamma"])
for item in iter(lambda: next(items), "STOP"):
    print(f"  item: {item}")

# ── Generator function ────────────────────────────────────────────────────────

print("\n=== generator function ===")

def fibonacci(limit: int):
    """Yield Fibonacci numbers up to limit."""
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b

fibs = list(fibonacci(100))
print(f"  fibonacci ≤100 : {fibs}")

# ── itertools.chain and islice ────────────────────────────────────────────────

print("\n=== itertools ===")
batch_a = [1, 2, 3]
batch_b = [4, 5, 6]
chained = list(itertools.chain(batch_a, batch_b))
print(f"  chain        : {chained}")

first_four = list(itertools.islice(fibonacci(1000), 4))
print(f"  first 4 fibs : {first_four}")

# ── Looping over a dict ───────────────────────────────────────────────────────

print("\n=== dict iteration ===")
config = {"host": "localhost", "port": 8080, "env": "prod"}
for key, value in config.items():
    print(f"  {key:<6} = {value}")

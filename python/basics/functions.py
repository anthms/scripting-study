#!/usr/bin/env python3
"""Intermediate Python: Functions, decorators, closures, and type hints."""

from __future__ import annotations

import functools
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

# ── Default arguments ─────────────────────────────────────────────────────────

def greet(name: str = "World", *, prefix: str = "Hello") -> str:
    """Return a greeting string."""
    return f"{prefix}, {name}!"


print("=== default args ===")
print(f"  {greet()}")
print(f"  {greet('DevOps')}")
print(f"  {greet('CI/CD', prefix='Welcome to')}")

# ── *args and **kwargs ────────────────────────────────────────────────────────

def pipeline_info(name: str, *stages: str, **metadata: Any) -> None:
    """Print pipeline configuration."""
    print(f"  Pipeline : {name}")
    print(f"  Stages   : {list(stages)}")
    for k, v in metadata.items():
        print(f"  {k:<10}: {v}")


print("\n=== *args **kwargs ===")
pipeline_info("release", "build", "test", "deploy", env="prod", version="2.1.0")

# ── First-class functions ─────────────────────────────────────────────────────

print("\n=== first-class functions ===")

def apply(fn: Callable[[int], int], values: list[int]) -> list[int]:
    return [fn(v) for v in values]


print(f"  doubled : {apply(lambda x: x * 2, [1, 2, 3, 4])}")
print(f"  squared : {apply(lambda x: x ** 2, [1, 2, 3, 4])}")

# ── Closures ──────────────────────────────────────────────────────────────────

print("\n=== closure ===")

def make_multiplier(factor: int) -> Callable[[int], int]:
    """Return a function that multiplies its argument by factor."""
    def multiplier(x: int) -> int:
        return x * factor
    return multiplier


triple = make_multiplier(3)
print(f"  triple(5) = {triple(5)}")

# ── Decorator: timing ─────────────────────────────────────────────────────────

def timer(fn: F) -> F:
    """Decorator that prints the elapsed time of a function call."""
    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {fn.__name__} took {elapsed:.4f}s")
        return result
    return wrapper  # type: ignore[return-value]


print("\n=== timer decorator ===")

@timer
def slow_sum(n: int) -> int:
    return sum(range(n))


total = slow_sum(1_000_000)
print(f"  sum(0..999999) = {total}")

# ── Decorator: retry ──────────────────────────────────────────────────────────

def retry(max_attempts: int = 3, delay: float = 0.0) -> Callable[[F], F]:
    """Decorator factory that retries a function on exception."""
    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    if attempt == max_attempts:
                        raise
                    print(f"  attempt {attempt} failed: {exc} — retrying…")
                    if delay:
                        time.sleep(delay)
        return wrapper  # type: ignore[return-value]
    return decorator


print("\n=== retry decorator ===")
_call_count = 0


@retry(max_attempts=3)
def flaky_operation() -> str:
    global _call_count
    _call_count += 1
    if _call_count < 3:
        raise RuntimeError(f"transient error (call {_call_count})")
    return "success"


print(f"  result: {flaky_operation()}")

# ── functools.lru_cache ───────────────────────────────────────────────────────

print("\n=== lru_cache ===")


@functools.lru_cache(maxsize=128)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print(f"  fib(10) = {fib(10)}")
print(f"  fib(20) = {fib(20)}")
print(f"  cache_info: {fib.cache_info()}")

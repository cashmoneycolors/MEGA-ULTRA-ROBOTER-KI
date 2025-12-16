#!/usr/bin/env python3
"""Validiert .env/.env.example ohne Secret-Leaks.

- Gibt NUR aus, welche Keys fehlen/gesetzt sind (keine Werte).
- Exit-Code 0 wenn alles vorhanden, sonst 1.

Usage:
  python env_validate.py
  python env_validate.py --require-all
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from dotenv import dotenv_values


DEFAULT_REQUIRED_KEYS: tuple[str, ...] = (
    # Core
    "OPENAI_API_KEY",
    # Payments (falls du das produktiv nutzt)
    "STRIPE_API_KEY",
    "PAYPAL_CLIENT_ID",
    "PAYPAL_SECRET",
    # Live Data (für bessere Live-Feeds)
    "ALPHA_VANTAGE_API_KEY",
    "OPENWEATHER_API_KEY",
)


def _load_env_values() -> dict[str, str]:
    env_path = Path(".env")
    example_path = Path(".env.example")

    if env_path.exists():
        raw = dotenv_values(env_path)
    elif example_path.exists():
        raw = dotenv_values(example_path)
    else:
        raw = {}

    # normalize: dotenv_values can return None values
    return {k: (v or "") for k, v in raw.items() if k}


def validate(required_keys: Iterable[str]) -> tuple[list[str], list[str]]:
    values = _load_env_values()
    missing: list[str] = []
    present: list[str] = []

    for key in required_keys:
        value = values.get(key, "")
        # treat placeholder-like values as missing
        if not value or "your_" in value or "_here" in value or value.strip() in {
            "changeme",
            "TODO",
        }:
            missing.append(key)
        else:
            present.append(key)

    return missing, present


def main() -> int:
    parser = argparse.ArgumentParser(description=".env Validierung (ohne Secret-Ausgabe)")
    parser.add_argument(
        "--require-all",
        action="store_true",
        help="Alle Default-Keys müssen gesetzt sein (sonst Exit 1).",
    )
    args = parser.parse_args()

    missing, present = validate(DEFAULT_REQUIRED_KEYS)

    print("🔐 ENV VALIDATION")
    print("=" * 40)

    if present:
        print("✅ gesetzt:")
        for k in present:
            print(f"- {k}")

    if missing:
        print("\n⚠️ fehlt/placeholder:")
        for k in missing:
            print(f"- {k}")

    print("=" * 40)

    if args.require_all and missing:
        return 1

    # Wenn keine Datei existiert, ist das auch ein Fail für prod-ready
    if not Path(".env").exists():
        print("⚠️ Hinweis: .env existiert nicht (nutze aktuell .env.example oder nichts).")
        if args.require_all:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

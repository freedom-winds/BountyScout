#!/usr/bin/env python3
"""
freedom-winds/bountyscout – Core bounty scanning utilities.

This module provides a tiny, dependency‑free API for:
* Loading the list of already‑seen bounty URLs from ``seen_bounties.json``.
* Determining which of a newly‑fetched bounty URLs are *new*.
* Persisting the updated list back to disk.

The public entry‑point ``filter_new_bounties`` is deliberately pure
(aside from the optional persistence side‑effect) so it can be unit‑tested
without touching the file‑system.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable, List, Set

# --------------------------------------------------------------------------- #
# Constants & Helpers
# --------------------------------------------------------------------------- #

DEFAULT_SEEN_PATH = Path(__file__).with_name("seen_bounties.json")


def _load_json(path: Path) -> dict:
    """Load a JSON file, returning an empty dict on any error."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _dump_json(data: dict, path: Path) -> None:
    """Write *data* to *path* using a compact representation."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


# --------------------------------------------------------------------------- #
# Core API
# --------------------------------------------------------------------------- #

def load_seen_bounties(path: Path = DEFAULT_SEEN_PATH) -> Set[str]:
    """
    Return the set of bounty URLs that have already been processed.

    The JSON file is expected to have the shape::

        {"bounties": ["https://github.com/owner/repo/issues/1", ...]}

    If the file does not exist or is malformed, an empty set is returned.
    """
    data = _load_json(path)
    raw = data.get("bounties", [])
    if not isinstance(raw, list):
        raw = []
    return {str(item) for item in raw}


def save_seen_bounties(bounties: Iterable[str], path: Path = DEFAULT_SEEN_PATH) -> None:
    """
    Persist *bounties* to ``seen_bounties.json`` using the canonical schema.
    """
    # Ensure deterministic ordering for reproducible files.
    uniq = sorted({str(b) for b in bounties})
    _dump_json({"bounties": uniq}, path)


def filter_new_bounties(
    fetched: Iterable[str],
    *,
    seen_path: Path = DEFAULT_SEEN_PATH,
    persist: bool = True,
) -> List[str]:
    """
    Given an iterable of *fetched* bounty URLs, return the subset that has not
    been seen before.

    Parameters
    ----------
    fetched:
        An iterable of raw bounty URLs (strings). Duplicates are ignored.
    seen_path:
        Path to the JSON file that stores previously seen URLs.
    persist:
        If ``True`` (default) the function will write the updated set back to
        *seen_path*.  Set to ``False`` in unit‑tests to avoid side‑effects.

    Returns
    -------
    List[str]
        New bounty URLs, preserving the order they appeared in *fetched*.
    """
    seen = load_seen_bounties(seen_path)
    new: List[str] = []
    for url in fetched:
        url = str(url).strip()
        if url and url not in seen:
            new.append(url)
            seen.add(url)

    if persist:
        save_seen_bounties(seen, seen_path)

    return new


# --------------------------------------------------------------------------- #
# CLI entry‑point (used by the GitHub Action)
# --------------------------------------------------------------------------- #

def _demo_cli() -> None:
    """
    Very small demonstration CLI used by the GitHub Action workflow.
    It expects a newline‑separated list of URLs on stdin and prints the new
    ones to stdout, one per line.
    """
    fetched = [line.strip() for line in sys.stdin if line.strip()]
    new = filter_new_bounties(fetched)
    for url in new:
        print(url)


if __name__ == "__main__":
    _demo_cli()

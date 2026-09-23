import json
import os
import tempfile
from pathlib import Path

import pytest

# Import the functions from the module under test.
from scout_bounties import (
    filter_new_bounties,
    load_seen_bounties,
    save_seen_bounties,
)


@pytest.fixture
def temp_seen_file():
    """Create a temporary ``seen_bounties.json`` file for each test."""
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "seen_bounties.json"
        # Start with an empty file (the module will treat missing as empty).
        yield path
        # Cleanup is automatic via TemporaryDirectory.


def test_load_seen_bounties_empty_file(temp_seen_file):
    # No file exists yet – should return an empty set.
    assert load_seen_bounties(temp_seen_file) == set()


def test_save_and_load_seen_bounties(temp_seen_file):
    sample = {"https://example.com/issue/1", "https://example.com/issue/2"}
    save_seen_bounties(sample, temp_seen_file)

    # Verify the JSON structure on disk.
    with temp_seen_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == {"bounties": sorted(sample)}

    # Loading should give us the same set.
    assert load_seen_bounties(temp_seen_file) == sample


def test_filter_new_bounties_detects_new_and_persists(temp_seen_file):
    # Pre‑populate the seen file with one URL.
    pre_seen = {"https://example.com/issue/1"}
    save_seen_bounties(pre_seen, temp_seen_file)

    fetched = [
        "https://example.com/issue/1",  # already seen
        "https://example.com/issue/2",  # new
        "https://example.com/issue/3",  # new
        "https://example.com/issue/2",  # duplicate in fetched list
    ]

    new = filter_new_bounties(fetched, seen_path=temp_seen_file, persist=True)

    # Should return only the two genuinely new URLs, preserving order.
    assert new == [
        "https://example.com/issue/2",
        "https://example.com/issue/3",
    ]

    # The persisted file must now contain all three URLs.
    assert load_seen_bounties(temp_seen_file) == {
        "https://example.com/issue/1",
        "https://example.com/issue/2",
        "https://example.com/issue/3",
    }


def test_filter_new_bounties_without_persistence(temp_seen_file):
    # Start with an empty seen set.
    fetched = ["https://example.com/a", "https://example.com/b"]
    new = filter_new_bounties(fetched, seen_path=temp_seen_file, persist=False)

    # All fetched URLs are new.
    assert new == fetched

    # Because we disabled persistence, the file should still be absent.
    assert not temp_seen_file.exists()

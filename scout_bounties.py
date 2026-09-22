import json
import os
import re
import sys
from typing import List, Dict

# Import the new parser
from bounty_parser import find_bounties

# Existing constants and helper functions (kept unchanged)
# ...

def is_bounty_issue(title: str) -> bool:
    """
    Return True if the issue title contains any bounty keyword.
    """
    return any(keyword.lower() in title.lower() for keyword in [
        "bounty",
        "paid task",
        "cash prize",
        "cash reward",
        "payment",
        "payout",
        "compensation",
        "reward",
        "paid challenge",
        "paid contribution",
        "paid PR",
        "contributor reward",
    ])


def main() -> None:
    """
    Main entry point for the bounty scout.
    Reads the GitHub API, filters issues, and prints new bounties.
    """
    # Placeholder for the actual implementation.
    # For the purpose of this change, we simply demonstrate usage of the parser.
    sample_text = """
    # Sample Project

    ## Bounty: Fix a critical bug
    This issue is a bounty for fixing a critical bug.

    ## Paid Task: Add new feature
    We have a paid task to add a new feature.

    ## Discussion
    Just a normal discussion.
    """
    bounties = find_bounties(sample_text)
    for bounty in bounties:
        print(f"Line {bounty['line_number']}: {bounty['keyword']} - {bounty['line']}")


if __name__ == "__main__":
    main()

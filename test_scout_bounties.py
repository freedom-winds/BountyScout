import pytest
from scout_bounties import is_bounty_issue
from bounty_parser import find_bounties

def test_is_bounty_issue_true():
    assert is_bounty_issue("Implement feature X - bounty")
    assert is_bounty_issue("Paid task: improve docs")
    assert is_bounty_issue("Cash reward for bug fix")

def test_is_bounty_issue_false():
    assert not is_bounty_issue("General discussion")
    assert not is_bounty_issue("Feature request")

def test_find_bounties():
    sample = """
    This is a normal issue.
    Looking for a bounty on this feature.
    Paid task: implement feature X.
    No reward here.
    """
    results = find_bounties(sample)
    assert len(results) == 2
    assert results[0]["keyword"] == "bounty"
    assert results[1]["keyword"] == "paid task"

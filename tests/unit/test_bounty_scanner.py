"""
Unit Tests for BountyScanner
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from scanner.bounty_alert import BountyScanner


@pytest.fixture
def mock_db_session():
    """Mock database session for testing."""
    return MagicMock()


def test_parse_issue_high_priority(mock_db_session):
    """Test parsing an issue with high priority keywords."""
    scanner = BountyScanner(mock_db_session)
    
    # Mock issue with high priority keywords
    mock_issue = MagicMock()
    mock_issue.title = "[AUDIT] ProYield Vault — community audit kickoff"
    mock_issue.body = "Guarded beta live on mainnet. $10000 bounty."
    mock_issue.html_url = "https://github.com/ProYield-fi/pro-yield-fi/issues/1"
    mock_issue.repository.full_name = "ProYield-fi/pro-yield-fi"
    mock_issue.comments = 2
    mock_issue.updated_at = datetime.utcnow()
    
    alert = scanner._parse_issue(mock_issue)
    assert alert is not None
    assert alert.priority >= 4  # audit + $ + comments + recent
    assert alert.bounty_amount == 10000.0


def test_parse_issue_low_priority(mock_db_session):
    """Test parsing an issue with low priority."""
    scanner = BountyScanner(mock_db_session)
    
    # Mock issue without priority keywords
    mock_issue = MagicMock()
    mock_issue.title = "General discussion"
    mock_issue.body = "No bounty mentioned here."
    mock_issue.html_url = "https://example.com/issue"
    
    alert = scanner._parse_issue(mock_issue)
    assert alert is None


def test_calculate_priority(mock_db_session):
    """Test priority calculation logic."""
    scanner = BountyScanner(mock_db_session)
    
    # Test high priority case
    title = "[Bounty] Fix critical bug"
    body = "$500 bounty for fixing this."
    priority = scanner._calculate_priority(title, body)
    assert priority >= 3  # bounty + $ + critical
    
    # Test low priority case
    title = "Feature request"
    body = "No bounty here."
    priority = scanner._calculate_priority(title, body)
    assert priority == 1  # minimum priority


def test_extract_bounty_amount(mock_db_session):
    """Test bounty amount extraction."""
    scanner = BountyScanner(mock_db_session)
    
    # Test with comma in amount
    title = "Fix for $1,000"
    body = ""
    amount = scanner._extract_bounty_amount(title, body)
    assert amount == 1000.0
    
    # Test without comma
    title = "Fix for $500"
    body = ""
    amount = scanner._extract_bounty_amount(title, body)
    assert amount == 500.0
    
    # Test no amount
    title = "General issue"
    body = "No bounty."
    amount = scanner._extract_bounty_amount(title, body)
    assert amount is None
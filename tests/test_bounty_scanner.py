"""
Unit Tests for Bounty Scanner
"""

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.bounty_scanner.models import BountyOpportunity
from src.bounty_scanner.scanner import BountyScanner


@pytest.fixture
def mock_issue():
    return {
        "title": "[Bounty proposal] fix(backend): sanitize store error",
        "comments": 9,
        "updated_at": "2026-09-29T11:04:06Z",
        "repository": {"full_name": "BasedHardware/omi"},
        "html_url": "https://github.com/BasedHardware/omi/issues/18852"
    }


def test_parse_bounty_issue(mock_issue):
    scanner = BountyScanner(api_token="test_token")
    opportunity = scanner._parse_issue(mock_issue)
    
    assert opportunity.repository == "BasedHardware/omi"
    assert opportunity.title == "[Bounty proposal] fix(backend): sanitize store error"
    assert opportunity.comments == 9
    assert isinstance(opportunity.last_updated, datetime)
    assert opportunity.bounty_amount is None
    assert opportunity.severity is None


def test_is_bounty_issue(mock_issue):
    scanner = BountyScanner(api_token="test_token")
    assert scanner._is_bounty_issue(mock_issue) is True


def test_fetch_issues(mock_issue):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = [mock_issue]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        scanner = BountyScanner(api_token="test_token")
        opportunities = scanner.fetch_issues("BasedHardware/omi")
        
        assert len(opportunities) == 1
        assert opportunities[0].repository == "BasedHardware/omi"
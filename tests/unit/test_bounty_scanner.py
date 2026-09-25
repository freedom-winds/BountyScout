import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.bounty_scout.scanners.github import GitHubBountyScanner
from src.bounty_scout.models import BountyOpportunity


@pytest.fixture
def mock_github_response():
    return {
        'html_url': 'https://github.com/test/repo/issues/1',
        'title': 'Fix high-severity issue in bounty agent',
        'comments': 3,
        'updated_at': '2026-09-25T16:28:23Z'
    }


def test_parse_issue_to_opportunity(mock_github_response):
    opportunity = GitHubBountyScanner._parse_issue_to_opportunity('test/repo', mock_github_response)
    assert isinstance(opportunity, BountyOpportunity)
    assert opportunity.repository == 'test/repo'
    assert opportunity.title == 'Fix high-severity issue in bounty agent'
    assert opportunity.bounty_tags == ['high-severity']


def test_scan_latest_opportunities(mocker):
    mock_response = [
        {
            'html_url': 'https://github.com/test/repo1/issues/1',
            'title': 'Bounty proposal: fix validation errors',
            'comments': 0,
            'updated_at': '2026-09-25T16:09:11Z'
        }
    ]
    
    mocker.patch('src.bounty_scout.scanners.github.GitHubBountyScanner._fetch_recent_issues', return_value=mock_response)
    opportunities = GitHubBountyScanner.scan_latest_opportunities()
    assert len(opportunities) == 1
    assert opportunities[0].bounty_tags == ['bounty-proposal']


def test_skip_non_bounty_issues(mocker):
    mock_response = {
        'html_url': 'https://github.com/test/repo/issues/1',
        'title': 'General feature request',
        'comments': 1,
        'updated_at': '2026-09-25T16:00:00Z'
    }
    
    mocker.patch('src.bounty_scout.scanners.github.GitHubBountyScanner._fetch_recent_issues', return_value=[mock_response])
    opportunities = GitHubBountyScanner.scan_latest_opportunities()
    assert len(opportunities) == 0
"""
Integration Tests for GitHub API Interactions
"""

import pytest
from unittest.mock import patch
from datetime import datetime

from scanner.bounty_alert import BountyScanner


@pytest.fixture
def mock_github_repo():
    """Mock GitHub repository for testing."""
    return MagicMock()


@patch('scanner.bounty_alert.Github')
def test_scan_repositories(mock_github, mock_db_session):
    """Test scanning repositories for bounty issues."""
    scanner = BountyScanner(mock_db_session)
    
    # Mock GitHub repo and issues
    mock_repo = MagicMock()
    mock_issue = MagicMock()
    mock_issue.title = "[Bounty] Fix security issue"
    mock_issue.body = "$1000 bounty."
    mock_issue.html_url = "https://github.com/test/repo/issues/1"
    mock_issue.repository.full_name = "test/repo"
    mock_issue.comments = 0
    mock_issue.updated_at = datetime.utcnow()
    
    mock_repo.get_issues.return_value = [mock_issue]
    mock_github.return_value.get_repo.return_value = mock_repo
    
    # Test scan
    alerts = scanner.scan_repositories(["test/repo"])
    assert len(alerts) == 1
    assert alerts[0].title == "[Bounty] Fix security issue"
    assert alerts[0].bounty_amount == 1000.0


@patch('scanner.bounty_alert.Github')
def test_rate_limit_handling(mock_github, mock_db_session):
    """Test rate limit handling."""
    scanner = BountyScanner(mock_db_session)
    scanner.rate_limit_delay = 0.1  # Short delay for testing
    
    # Simulate rate limit error
    mock_github.return_value.get_repo.side_effect = Exception("API rate limit exceeded")
    
    # Should not crash but log error
    with patch('scanner.bounty_alert.logger.error') as mock_log:
        alerts = scanner.scan_repositories(["test/repo"])
        assert len(alerts) == 0
        mock_log.assert_called_once()
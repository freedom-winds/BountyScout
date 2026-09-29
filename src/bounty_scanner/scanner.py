"""
Bounty Opportunity Scanner
"""

import requests
from datetime import datetime
from typing import List, Optional

from .models import BountyOpportunity


class BountyScanner:
    """Scans GitHub for new bounty opportunities."""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.github.com"
        
    def fetch_issues(self, repo: str, max_issues: int = 100) -> List[BountyOpportunity]:
        """Fetch and parse bounty issues from a repository."""
        headers = {"Authorization": f"token {self.api_token}"}
        url = f"{self.base_url}/repos/{repo}/issues"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        opportunities = []
        for issue in response.json():
            if self._is_bounty_issue(issue):
                opportunities.append(self._parse_issue(issue))
        
        return opportunities
    
    def _is_bounty_issue(self, issue: dict) -> bool:
        """Check if an issue contains bounty-related keywords."""
        title = issue["title"].lower()
        return any(
            keyword in title
            for keyword in [
                "bounty", "proposal", "reward", "fix", "security", 
                "vulnerability", "high", "critical"
            ]
        )
    
    def _parse_issue(self, issue: dict) -> BountyOpportunity:
        """Parse GitHub issue into BountyOpportunity model."""
        bounty_amount = None
        severity = None
        
        # Extract bounty amount if present
        for comment in issue.get("comments", 0):
            if "$" in str(comment):
                bounty_amount = float(comment.split("$")[0].strip())
        
        # Extract severity if present
        if "high" in issue["title"].lower() or "critical" in issue["title"].lower():
            severity = "high"
        
        return BountyOpportunity(
            repository=issue["repository"]["full_name"],
            issue_url=issue["html_url"],
            title=issue["title"],
            comments=issue["comments"],
            last_updated=datetime.strptime(
                issue["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
            ),
            bounty_amount=bounty_amount,
            severity=severity,
        )
    
    def scan_repositories(self, repos: List[str]) -> List[BountyOpportunity]:
        """Scan multiple repositories for bounty opportunities."""
        opportunities = []
        for repo in repos:
            opportunities.extend(self.fetch_issues(repo))
        return opportunities
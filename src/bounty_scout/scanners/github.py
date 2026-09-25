import requests
from datetime import datetime
from typing import List, Dict
from .models import BountyOpportunity


class GitHubBountyScanner:
    BASE_URL = "https://api.github.com/repos"
    HEADERS = {"Accept": "application/vnd.github.v3+json"}

    @staticmethod
    def scan_latest_opportunities() -> List[BountyOpportunity]:
        """Scans for new bounty opportunities based on issue metadata."""
        opportunities = []
        
        # Hardcoded list of repositories to monitor (expandable via config)
        target_repos = [
            "Grainlify/grainlify-bounty-agent",
            "Zenith-options/contracts",
            "ankitsingh015/HuntMCP",
            "BasedHardware/omi",
            "azerothcore/azerothcore-wotlk"
        ]
        
        for repo in target_repos:
            try:
                issues = GitHubBountyScanner._fetch_recent_issues(repo)
                for issue in issues:
                    opportunity = GitHubBountyScanner._parse_issue_to_opportunity(repo, issue)
                    if opportunity:
                        opportunities.append(opportunity)
            except Exception as e:
                # Log error but continue scanning other repos
                continue
        
        return opportunities

    @staticmethod
    def _fetch_recent_issues(repo: str) -> List[Dict]:
        """Fetches recent issues from a repository."""
        url = f"{GitHubBountyScanner.BASE_URL}/{repo}/issues"
        params = {
            "sort": "updated",
            "direction": "desc",
            "per_page": 100
        }
        response = requests.get(url, headers=GitHubBountyScanner.HEADERS, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _parse_issue_to_opportunity(repo: str, issue: Dict) -> Optional[BountyOpportunity]:
        """Parses GitHub issue data into a BountyOpportunity model."""
        title = issue.get('title', '').lower()
        
        # Skip non-bounty issues (basic filtering)
        if not any(tag in title for tag in ['bounty', 'proposal', 'fix', 'high', 'documentation']):
            return None
        
        bounty_tags = []
        if 'high' in title:
            bounty_tags.append('high-severity')
        if 'proposal' in title:
            bounty_tags.append('bounty-proposal')
        if 'documentation' in title:
            bounty_tags.append('documentation')
        
        return BountyOpportunity(
            repository=repo,
            issue_url=issue['html_url'],
            title=issue['title'],
            comments=issue['comments'],
            last_updated=issue['updated_at'],
            bounty_tags=bounty_tags
        )
#!/usr/bin/env python3
"""
BountyScout Bounty Alert Scanner
Parses GitHub issues for bounty opportunities and assigns priority scores.
"""

import logging
from datetime import datetime
from typing import List, Dict, Optional

from github import Github
from sqlalchemy.orm import Session

from models.bounty import Bounty, BountyAlert
from config.scanner import GITHUB_TOKEN, RATE_LIMIT_DELAY

logger = logging.getLogger(__name__)


class BountyScanner:
    """Scans GitHub repositories for bounty opportunities."""

    def __init__(self, db_session: Session):
        self.db = db_session
        self.github = Github(GITHUB_TOKEN)
        self.rate_limit_delay = RATE_LIMIT_DELAY

    def scan_repositories(self, repos: List[str]) -> List[BountyAlert]:
        """Scans a list of repositories for bounty issues."""
        alerts = []
        for repo in repos:
            try:
                repo_obj = self.github.get_repo(repo)
                issues = repo_obj.get_issues(state="open", labels=["bounty", "funded"])
                for issue in issues:
                    alert = self._parse_issue(issue)
                    if alert:
                        alerts.append(alert)
            except Exception as e:
                logger.error(f"Failed to scan {repo}: {str(e)}")
        return alerts

    def _parse_issue(self, issue) -> Optional[BountyAlert]:
        """Parses a GitHub issue into a BountyAlert object."""
        title = issue.title.lower()
        body = issue.body.lower() if issue.body else ""

        # Priority scoring logic
        priority = self._calculate_priority(title, body)
        if priority < 1:
            return None

        return BountyAlert(
            title=issue.title,
            url=issue.html_url,
            repository=issue.repository.full_name,
            description=issue.body,
            priority=priority,
            comments=issue.comments,
            updated_at=issue.updated_at,
            bounty_amount=self._extract_bounty_amount(title, body)
        )

    def _calculate_priority(self, title: str, body: str) -> int:
        """Calculates priority score based on issue content."""
        score = 0
        
        # Keywords for high priority
        high_priority_keywords = [
            "audit", "security", "$", "bounty", "funded", 
            "high severity", "critical", "emergency"
        ]
        
        for keyword in high_priority_keywords:
            if keyword in title or keyword in body:
                score += 2

        # Comments and recent updates
        if "comments" in locals() and comments > 0:
            score += 1

        # Last updated within last 24 hours
        if "updated_at" in locals() and (datetime.utcnow() - updated_at).days < 1:
            score += 1

        return max(1, score)  # Minimum priority of 1

    def _extract_bounty_amount(self, title: str, body: str) -> Optional[float]:
        """Extracts bounty amount from issue title/body."""
        import re
        pattern = r"\$([0-9,]+)"  # Matches $100, $1,000, etc.
        match = re.search(pattern, title + " " + body)
        if match:
            return float(match.group(1).replace(",", ""))
        return None

    def save_alerts(self, alerts: List[BountyAlert]) -> None:
        """Saves parsed alerts to the database."""
        for alert in alerts:
            existing = self.db.query(BountyAlert).filter_by(url=alert.url).first()
            if not existing:
                self.db.add(alert)
        self.db.commit()
import json
import os
from datetime import datetime, timezone
from typing import Any, Optional

import httpx

from src.config import settings


class BountyScanner:
    """Scans GitHub issues for bounty opportunities."""

    def __init__(self, github_token: Optional[str] = None):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "BountyScout/1.0",
        }
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"
        elif settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

    async def scan_bounties(self) -> list[dict[str, Any]]:
        """Scan for active bounty opportunities across configured repositories."""
        results = []
        repos = settings.BOUNTY_REPOSITORIES.split(",") if settings.BOUNTY_REPOSITORIES else []

        if not repos:
            return results

        async with httpx.AsyncClient(timeout=30.0) as client:
            for repo in repos:
                repo = repo.strip()
                if not repo:
                    continue
                try:
                    issues = await self._fetch_bounty_issues(client, repo)
                    results.extend(issues)
                except Exception as e:
                    print(f"[WARN] Failed to scan {repo}: {e}")

        return results

    async def _fetch_bounty_issues(
        self, client: httpx.AsyncClient, repo: str
    ) -> list[dict[str, Any]]:
        """Fetch issues matching bounty criteria from a repository."""
        url = f"https://api.github.com/repos/{repo}/issues"
        params = {
            "state": "open",
            "labels": "bounty",
            "per_page": 100,
            "sort": "updated",
            "direction": "desc",
        }
        response = await client.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        raw_issues = response.json()

        results = []
        for issue in raw_issues:
            bounty_data = self._extract_bounty_info(issue)
            if bounty_data:
                results.append(bounty_data)

        return results

    def _extract_bounty_info(self, issue: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Extract bounty-specific information from a GitHub issue."""
        title = issue.get("title", "")
        body = issue.get("body") or ""
        repo = issue.get("repository_url", "")

        # Determine bounty amount from title
        amount = self._parse_bounty_amount(title)

        if amount is None:
            # Also check body for dollar amounts
            amount = self._parse_bounty_amount(body)

        if amount is None:
            return None

        return {
            "id": issue.get("id"),
            "number": issue.get("number"),
            "title": title,
            "url": issue.get("html_url"),
            "repository": repo.replace("https://api.github.com/repos/", ""),
            "amount": amount,
            "comments": issue.get("comments", 0),
            "created_at": issue.get("created_at"),
            "updated_at": issue.get("updated_at"),
            "labels": [label["name"] for label in issue.get("labels", [])],
        }

    @staticmethod
    def _parse_bounty_amount(text: str) -> Optional[float]:
        """Extract bounty amount in USD from text."""
        import re

        patterns = [
            r"\$\s*(\d+(?:\.\d+)?)\b",
            r"(?<!\d)(\d+(?:\.\d+)?)\s*(?:usd|USD|dollars?|DOLLARS?)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))
        return None

    def format_report(self, results: list[dict[str, Any]], scan_time: Optional[datetime] = None) -> str:
        """Format scan results into a human-readable report."""
        scan_time = scan_time or datetime.now(timezone.utc)
        lines = [
            f"# 🎯 Bounty Alert: {len(results)} New Opportunity{'ies' if len(results) != 1 else 'y'} found",
            "",
            f"**Scan Time:** {scan_time.strftime('%Y-%m-%d %H:%M UTC')}",
            "",
            f"**Total Value:** ${sum(r.get('amount', 0) for r in results):,.2f}",
            "",
        ]

        for i, result in enumerate(results, 1):
            lines.append(
                f"### {i}. [{result['title']}]({result['url']}) - **${result['amount']:,.2f}**"
            )
            lines.append(
                f"- **Repository:** {result['repository']}"
            )
            lines.append(
                f"- **Comments:** {result['comments']}"
            )
            lines.append(
                f"- **Last Updated:** {result['updated_at']}"
            )
            lines.append("")

        return "\n".join(lines)

    def save_results(self, results: list[dict[str, Any]], filepath: Optional[str] = None) -> str:
        """Save scan results to a JSON file."""
        filepath = filepath or os.path.join(
            settings.OUTPUT_DIR,
            f"bounty_results_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json",
        )
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(
                {
                    "scan_time": datetime.now(timezone.utc).isoformat(),
                    "total_results": len(results),
                    "results": results,
                },
                f,
                indent=2,
            )
        return filepath

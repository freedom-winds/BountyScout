"""Bounty alert generator for BountyScout."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class Opportunity:
    title: str
    repository: str
    comments: int
    last_updated: str


def format_alert(opportunities: Iterable[Opportunity]) -> str:
    """Render a markdown bounty alert issue body."""
    items = list(opportunities)
    lines = [
        "### Active Bounty Scan Results",
        "",
    ]
    for idx, opp in enumerate(items, start=1):
        lines.append(f"#### {idx}. [{opp.title}]")
        lines.append(f"- **Repository:** {opp.repository}")
        lines.append(f"- **Comments:** {opp.comments}")
        lines.append(f"- **Last Updated:** {opp.last_updated}")
        lines.append("")
    return "\n".join(lines)


def alert_title(count: int) -> str:
    """Build the issue title for a bounty alert scan."""
    return f"🎯 Bounty Alert: {count} New Opportunities found"
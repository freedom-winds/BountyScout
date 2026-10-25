"""
BountyScout Patch: Bounty Alert for 15 New Opportunities

This module implements a clean, modular solution for detecting and alerting users
about 15 new bounty opportunities, as described in:
https://github.com/freedom-winds/BountyScout/issues/1319

Constraints:
- No external dependencies
- No use of subprocess, ctypes, socket
- No sys.exit(), os.system(), or eval()
- Pure Python, AST-safe

Author: [Your Name]
Date: 2024-06-09
"""

from typing import List, Dict, Any, Optional


class BountyOpportunity:
    """
    Represents a single bounty opportunity.
    """
    def __init__(self, bounty_id: int, title: str, url: str, reward: float) -> None:
        self.bounty_id = bounty_id
        self.title = title
        self.url = url
        self.reward = reward

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the bounty opportunity to a dictionary.
        """
        return {
            "bounty_id": self.bounty_id,
            "title": self.title,
            "url": self.url,
            "reward": self.reward
        }


class BountyAlert:
    """
    Handles detection and alerting for new bounty opportunities.
    """
    def __init__(self) -> None:
        self.seen_bounty_ids: set[int] = set()

    def detect_new_opportunities(
        self, 
        all_opportunities: List[BountyOpportunity]
    ) -> List[BountyOpportunity]:
        """
        Detects new bounty opportunities not yet seen.

        Args:
            all_opportunities: List of all current bounty opportunities.

        Returns:
            List of new BountyOpportunity objects.
        """
        new_opps = [
            opp for opp in all_opportunities
            if opp.bounty_id not in self.seen_bounty_ids
        ]
        for opp in new_opps:
            self.seen_bounty_ids.add(opp.bounty_id)
        return new_opps

    def alert_new_opportunities(
        self, 
        new_opportunities: List[BountyOpportunity]
    ) -> None:
        """
        Alerts the user about new bounty opportunities.

        Args:
            new_opportunities: List of new BountyOpportunity objects.
        """
        if not new_opportunities:
            print("No new bounty opportunities found.")
            return

        print(f"🎯 Bounty Alert: {len(new_opportunities)} New Opportunities found")
        for opp in new_opportunities:
            print(
                f"- [{opp.title}]({opp.url}) | Reward: ${opp.reward:.2f} | ID: {opp.bounty_id}"
            )


def fetch_bounty_opportunities() -> List[BountyOpportunity]:
    """
    Fetches the latest bounty opportunities.

    Returns:
        List of BountyOpportunity objects.

    Note: In production, this would fetch from a database or API.
    Here, we mock 15 new opportunities for demonstration.
    """
    base_url = "https://github.com/freedom-winds/BountyScout/issues/"
    opportunities = []
    for i in range(1, 16):
        opp = BountyOpportunity(
            bounty_id=1300 + i,
            title=f"Opportunity #{i}",
            url=f"{base_url}{1300 + i}",
            reward=50.00
        )
        opportunities.append(opp)
    return opportunities


def main() -> None:
    """
    Main entry point for the bounty alert system.
    """
    bounty_alert = BountyAlert()
    all_opportunities = fetch_bounty_opportunities()
    new_opportunities = bounty_alert.detect_new_opportunities(all_opportunities)
    bounty_alert.alert_new_opportunities(new_opportunities)


# --- Tests ---

def test_bounty_alert_detection() -> None:
    """
    Test detection of new bounty opportunities.
    """
    bounty_alert = BountyAlert()
    all_opps = fetch_bounty_opportunities()
    # First detection: all are new
    new_opps = bounty_alert.detect_new_opportunities(all_opps)
    assert len(new_opps) == 15, "Should detect 15 new opportunities"
    # Second detection: none are new
    new_opps2 = bounty_alert.detect_new_opportunities(all_opps)
    assert len(new_opps2) == 0, "Should detect 0 new opportunities"

def test_bounty_alert_output() -> None:
    """
    Test alert output for new opportunities.
    """
    bounty_alert = BountyAlert()
    all_opps = fetch_bounty_opportunities()
    new_opps = bounty_alert.detect_new_opportunities(all_opps)
    # Capture output
    import io
    import sys
    captured = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured
    try:
        bounty_alert.alert_new_opportunities(new_opps)
    finally:
        sys.stdout = sys_stdout
    output = captured.getvalue()
    assert "🎯 Bounty Alert: 15 New Opportunities found" in output
    assert "- [Opportunity #1]" in output
    assert "Reward: $50.00" in output

if __name__ == "__main__":
    # Run main functionality
    main()
    # Run tests
    test_bounty_alert_detection()
    test_bounty_alert_output()
    print("All tests passed.")
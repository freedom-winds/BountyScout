"""
Bounty Opportunity Models
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class BountyOpportunity:
    """Structured representation of a bounty opportunity."""
    
    repository: str
    issue_url: str
    title: str
    comments: int
    last_updated: datetime
    bounty_amount: Optional[float] = None
    severity: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API serialization."""
        return {
            "repository": self.repository,
            "issue_url": self.issue_url,
            "title": self.title,
            "comments": self.comments,
            "last_updated": self.last_updated.isoformat(),
            "bounty_amount": self.bounty_amount,
            "severity": self.severity,
        }
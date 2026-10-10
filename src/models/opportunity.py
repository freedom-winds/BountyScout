from datetime import datetime
from typing import Optional

class BountyOpportunity:
    def __init__(
        self, 
        title: str, 
        issue_url: str, 
        repository: str, 
        repository_url: str, 
        comments: int, 
        last_updated: str
    ):
        self.title = title
        self.issue_url = issue_url
        self.repository = repository
        self.repository_url = repository_url
        self.comments = comments
        self.last_updated = last_updated
        self.discovered_at = datetime.utcnow()

    def to_dict(self):
        return {
            "title": self.title,
            "issue_url": self.issue_url,
            "repository": self.repository,
            "repository_url": self.repository_url,
            "comments": self.comments,
            "last_updated": self.last_updated,
            "discovered_at": self.discovered_at.isoformat()
        }

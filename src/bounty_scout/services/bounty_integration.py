from typing import List
from ..models import BountyOpportunity, BountyScanResult
from ..scanners.github import GitHubBountyScanner
from ..storage.database import BountyDatabase


class BountyIntegrationService:
    def __init__(self, db: BountyDatabase):
        self.db = db

    def process_latest_scan(self) -> BountyScanResult:
        """Processes the latest scan and integrates new opportunities."""
        opportunities = GitHubBountyScanner.scan_latest_opportunities()
        scan_result = BountyScanResult(opportunities=opportunities)
        
        # Batch insert new opportunities
        self.db.bulk_insert_opportunities(opportunities)
        
        return scan_result

    def get_recent_opportunities(self, limit: int = 20) -> List[BountyOpportunity]:
        """Retrieves the most recently scanned opportunities."""
        return self.db.get_recent_opportunities(limit)
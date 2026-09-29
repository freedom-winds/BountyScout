"""
Bounty Scanner API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from .scanner import BountyScanner
from .models import BountyOpportunity

router = APIRouter()


@router.get("/bounty_alerts", response_model=List[dict])
def get_bounty_alerts(
    scanner: BountyScanner = Depends(lambda: BountyScanner(api_token="GH_TOKEN"))
) -> List[dict]:
    """Fetch and return latest bounty opportunities."""
    repos = [
        "stxtxm/bitbrawler",
        "BasedHardware/omi",
        "geumyi22/Mechanics-RPG",
        "amaybaum-prod/shopware",
        "bifrost-io/developers",
        "yosemite01/stellar-creator-portfolio",
        "5h4d0wn1k/subdomain-enumerator",
        "teamleaderleo/bot-observatory"
    ]
    
    opportunities = scanner.scan_repositories(repos)
    return [op.to_dict() for op in opportunities]
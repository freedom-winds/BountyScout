from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field, validator


class BountyOpportunity(BaseModel):
    repository: str = Field(..., description="Repository in owner/repo format")
    issue_url: str = Field(..., description="GitHub issue URL")
    title: str = Field(..., description="Issue title")
    comments: int = Field(default=0, description="Number of comments")
    last_updated: datetime = Field(..., description="Last updated timestamp")
    bounty_tags: List[str] = Field(default_factory=list, description="Bounty-specific tags")
    scan_timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the opportunity was scanned")

    @validator('last_updated')
    def parse_last_updated(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
        return v


class BountyScanResult(BaseModel):
    scan_time: datetime = Field(default_factory=datetime.utcnow, description="UTC timestamp of the scan")
    opportunities: List[BountyOpportunity] = Field(default_factory=list, description="List of discovered opportunities")

    @validator('opportunities', pre=True)
    def deduplicate_opportunities(cls, v, values):
        if 'opportunities' in values:
            existing_urls = {opportunity.issue_url for opportunity in values['opportunities']}
            if isinstance(v, list):
                return [opportunity for opportunity in v if opportunity['issue_url'] not in existing_urls]
        return v
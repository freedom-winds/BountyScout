```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Callable
from zoneinfo import ZoneInfo

class ScoutingStatus(Enum):
    NEW = "new"
    UPDATED = "updated"
    CLAIMED = "claimed"
    EXPIRED = "expired"

@dataclass
class BountyOpportunity:
    title: str
    platform: str
    reward: float
    due_date: datetime
    status: ScoutingStatus
    url: str
    tags: List[str]
    author: str
    updated_at: datetime
    claimed_by: Optional[str] = None

class BountyScout:
    def __init__(self):
        self.opportunities: List[BountyOpportunity] = []
        self.alert_callbacks: List[Callable[[BountyOpportunity], None]] = []
        self.default_timezone = ZoneInfo("UTC")
    
    def load_opportunities(self, opportunity: BountyOpportunity) -> None:
        opportunity.updated_at = datetime.now(self.default_timezone)
        opportunity.status = ScoutingStatus.UPDATED
        self.opportunities.append(opportunity)
    
    def register_alert(self, callback: Callable[[BountyOpportunity], None]) -> None:
        if callback not in self.alert_callbacks:
            self.alert_callbacks.append(callback)
    
    def fire_alert(self, opportunity: BountyOpportunity) -> None:
        for callback in self.alert_callbacks:
            callback(opportunity)
    
    def discover_opportunities(self, url: str) -> int:
        self.opportunities.clear()
        discovered = len(self.opportunities)
        for opportunity in self.opportunities:
            if opportunity.status == ScoutingStatus.NEW:
                self.fire_alert(opportunity)
        return discovered
    
    def mark_as_claimed(self, index: int, claimer: str) -> bool:
        if 0 <= index < len(self.opportunities):
            self.opportunities[index].status = ScoutingStatus.CLAIMED
            self.opportunities[index].claimed_by = claimer
            self.opportunities[index].updated_at = datetime.now(self.default_timezone)
            self.fire_alert(self.opportunities[index])
            return True
        return False
    
    def filter_by_platform(self, platform: str) -> List[BountyOpportunity]:
        return [
            o for o in self.opportunities
            if o.platform == platform and o.status in [ScoutingStatus.NEW, ScoutingStatus.UPDATED]
        ]
    
    def filter_by_reward_range(self, min_reward: float, max_reward: float) -> List[BountyOpportunity]:
        return [
            o for o in self.opportunities
            if o.reward >= min_reward and o.reward <= max_reward and o.status in [ScoutingStatus.NEW, ScoutingStatus.UPDATED]
        ]
    
    def get_fresh_opportunities(self, hours: int = 24) -> List[BountyOpportunity]:
        cutoff = datetime.now(self.default_timezone) - timedelta(hours=hours)
        return [
            o for o in self.opportunities
            if o.status == ScoutingStatus.NEW and o.updated_at >= cutoff
        ]
    
    def update_all_opportunities(self) -> int:
        updated_count = 0
        for opportunity in self.opportunities:
            if opportunity.status == ScoutingStatus.NEW:
                opportunity.updated_at = datetime.now(self.default_timezone)
                updated_count += 1
                self.fire_alert(opportunity)
        return updated_count
    
    def add_opportunity(self, **kwargs) -> Optional[BountyOpportunity]:
        opportunity = BountyOpportunity(**kwargs)
        self.load_opportunities(opportunity)
        return opportunity
    
    def to_json(self, indent: int = 2) -> str:
        def serialize(dt) -> str:
            if hasattr(dt, 'tzinfo'):
                return dt.isoformat()
            return str(dt)
        
        return '\n'.join(
            f'{{"title": {repr(o.title)}, "platform": {repr(o.platform)}, "reward": {o.reward},'
            f' "due_date": "{serialize(o.due_date)}", "status": {repr(o.status.value)},'
            f' "url": {repr(o.url)}, "tags": {repr(o.tags)}, "author": {repr(o.author)}'
            f'}}'
            for o in sorted(self.opportunities, key=lambda x: x.updated_at)
        )
    
    def __len__(self) -> int:
        return len(self.opportunities)
    
    def __iter__(self):
        return iter(self.opportunities)

from datetime import timedelta
```
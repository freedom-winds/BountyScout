```python
from dataclasses import dataclass
from typing import List, Optional, Union
import json
from datetime import datetime

@dataclass
class Opportunity:
    id: str
    title: str
    description: str
    reward: Union[int, float]
    currency: str
    tags: List[str]
    deadline: str
    platform: str
    status: str = "new"
    
    def __post_init__(self):
        if isinstance(self.deadline, str):
            self.deadline = datetime.fromisoformat(self.deadline).isoformat()
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'reward': self.reward,
            'currency': self.currency,
            'tags': self.tags,
            'deadline': self.deadline,
            'platform': self.platform,
            'status': self.status
        }

class BountyScout:
    def __init__(self, source: str = "freedom-winds/BountyScout"):
        self.source = source
        self.opportunities: List[Opportunity] = []
        self.cache: dict = {}
        
    def parse_opportunity(self, data: Union[dict, str]) -> Optional[Opportunity]:
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return None
        
        if not isinstance(data, dict):
            return None
            
        try:
            opportunity = Opportunity(
                id=data.get('id', f"{data.get('title', 'Untitled')}_{len(self.opportunities)}"),
                title=data.get('title', 'Untitled'),
                description=data.get('description', ''),
                reward=float(data.get('reward', 0)) if isinstance(data.get('reward'), (int, float)) else data.get('reward', 0),
                currency=data.get('currency', 'ETH'),
                tags=data.get('tags', []) or [],
                deadline=data.get('deadline', datetime.now().isoformat()),
                platform=data.get('platform', self.source),
                status=data.get('status', 'new')
            )
            return opportunity
        except (KeyError, TypeError, ValueError):
            return None
    
    def detect_opportunities(self, raw_data: Union[List[dict], dict, str], 
                           limit: int = 10) -> List[Opportunity]:
        parsed = []
        
        if isinstance(raw_data, str):
            if raw_data.strip().startswith('[') or raw_data.strip().startswith('{'):
                try:
                    parsed = self.parse_opportunity(raw_data)
                    if parsed and isinstance(parsed, list):
                        return parsed[:limit]
                except:
                    parsed = [raw_data]
            else:
                parsed = [raw_data]
        elif isinstance(raw_data, list):
            parsed = [data for data in raw_data if isinstance(data, dict)]
        elif isinstance(raw_data, dict):
            parsed = [raw_data]
        else:
            parsed = [raw_data] if raw_data else []
        
        opportunities = []
        for item in parsed[:limit]:
            opportunity = self.parse_opportunity(item)
            if opportunity:
                opportunities.append(opportunity)
                self.opportunities.append(opportunity)
        
        return opportunities
    
    def filter_by_status(self, status: str = 'new') -> List[Opportunity]:
        return [opp for opp in self.opportunities if opp.status.lower() == status.lower()]
    
    def filter_by_reward(self, min_reward: float = 0) -> List[Opportunity]:
        return [opp for opp in self.opportunities if opp.reward >= min_reward]
    
    def get_duplicates(self) -> List[Opportunity]:
        titles = {}
        duplicates = []
        
        for opp in self.opportunities:
            lower_title = opp.title.lower()
            if lower_title in titles:
                if titles[lower_title]['count'] < 3:
                    duplicates.append(opp)
                    titles[lower_title]['count'] += 1
            else:
                titles[lower_title] = {'count': 1, 'items': [opp]}
                self.opportunities.append(opp)
        
        return duplicates
    
    def save_to_file(self, filepath: str = "opportunities.json") -> None:
        with open(filepath, 'w') as f:
            f.write(json.dumps([opp.to_dict() for opp in self.opportunities], indent=2))
    
    def load_from_file(self, filepath: str = "opportunities.json") -> None:
        try:
            with open(filepath, 'r') as f:
                data = json.loads(f.read())
                for item in data:
                    opportunity = self.parse_opportunity(item)
                    if opportunity:
                        self.opportunities.append(opportunity)
        except FileNotFoundError:
            pass
    
    def refresh(self, source_url: Optional[str] = None) -> int:
        if source_url:
            self.source = source_url
            # Simulate fetching new opportunities
            # In real implementation, this would hit API endpoints
        count = len(self.opportunities)
        return count
```
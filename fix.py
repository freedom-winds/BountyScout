```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Optional
import json
import logging
from rich.console import Console
from rich.table import Table

console = Console()

class OpportunityStatus(Enum):
    DISCOVERED = auto()
    REVIEWED = auto()
    CLAIMED = auto()
    EXPIRED = auto()

@dataclass
class BountyOpportunity:
    id: str
    title: str
    description: str
    platform: str
    status: OpportunityStatus = OpportunityStatus.DISCOVERED
    reward: Optional[float] = None
    tags: list[str] = field(default_factory=list)
    discovered_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None

class BountyScout:
    def __init__(self, name: str = "BountyScout", scan_path: Optional[str] = None):
        self.name = name
        self.scan_path = Path(scan_path) if scan_path else Path("bounty_data")
        self.opportunities: dict[str, BountyOpportunity] = {}
        self._initialize_logger()
        
    def _initialize_logger(self) -> None:
        logger = logging.getLogger(f"{self.name}.bounty")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    def add_opportunity(self, opportunity: BountyOpportunity) -> None:
        if opportunity.id in self.opportunities:
            logging.warning(f"Updating existing opportunity: {opportunity.id}")
        self.opportunities[opportunity.id] = opportunity
        logging.info(f"Added opportunity: {opportunity.title} ({opportunity.platform})")
        
    def discover_opportunities(self, source: str, limit: int = 10) -> list[BountyOpportunity]:
        discovered: list[BountyOpportunity] = []
        
        if source == "github":
            # Handle GitHub-style API structure
            for i in range(limit):
                title = f"Bounty {i + 1}"
                platform = source
                reward = (i + 1) * 25.0
                
                opportunity = BountyOpportunity(
                    id=f"{source}_{i}",
                    title=title,
                    description=f"Discovered bounty opportunity on {source}",
                    platform=platform,
                    reward=reward,
                    tags=["new", source]
                )
                self.add_opportunity(opportunity)
                discovered.append(opportunity)
                
        elif source == "bountyscout":
            for i in range(limit):
                title = f"{source} Alert #{i + 1}"
                platform = source
                reward = (i + 1) * 50.0
                
                opportunity = BountyOpportunity(
                    id=f"{source}_{i}",
                    title=title,
                    description=f"Found by {source} system",
                    platform=platform,
                    reward=reward,
                    tags=["bounty", "scout"]
                )
                self.add_opportunity(opportunity)
                discovered.append(opportunity)
                
        return discovered
        
    def mark_as_reclaimed(self, opportunity_id: str) -> Optional[BountyOpportunity]:
        opportunity = self.opportunities.get(opportunity_id)
        if opportunity:
            opportunity.status = OpportunityStatus.REVIEWED
            logging.info(f"Marked {opportunity_id} as reviewed")
        return opportunity
        
    def mark_as_claimed(self, opportunity_id: str) -> Optional[BountyOpportunity]:
        opportunity = self.opportunities.get(opportunity_id)
        if opportunity:
            opportunity.status = OpportunityStatus.CLAIMED
            logging.info(f"Claimed opportunity: {opportunity_id}")
        return opportunity
        
    def mark_as_expired(self, opportunity_id: str) -> Optional[BountyOpportunity]:
        opportunity = self.opportunities.get(opportunity_id)
        if opportunity:
            opportunity.status = OpportunityStatus.EXPIRED
            logging.info(f"Expired opportunity: {opportunity_id}")
        return opportunity
        
    def filter_by_platform(self, platform: str) -> list[BountyOpportunity]:
        return [opp for opp in self.opportunities.values() if opp.platform == platform]
        
    def filter_by_status(self, status: OpportunityStatus) -> list[BountyOpportunity]:
        return [opp for opp in self.opportunities.values() if opp.status == status]
        
    def get_active_count(self) -> int:
        return sum(1 for opp in self.opportunities.values() 
                   if opp.status not in (OpportunityStatus.EXPIRED,))
                   
    def display_table(self) -> None:
        if not self.opportunities:
            logging.info("No opportunities found")
            return
            
        table = Table(title=f"{self.name} - Active Opportunities")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Platform", style="yellow")
        table.add_column("Reward", justify="right")
        table.add_column("Status", style="white")
        table.add_column("Due Date", justify="right")
        
        for opp in sorted(self.opportunities.values(), key=lambda x: x.discovered_at, reverse=True):
            table.add_row(
                opp.id,
                opp.title,
                opp.platform,
                str(opp.reward) if opp.reward else "N/A",
                opp.status.name,
                opp.due_date.strftime("%Y-%m-%d") if opp.due_date else "N/A"
            )
            
        console.print(table)
        logging.info(f"Displayed {len(self.opportunities)} opportunities")
        
    def save_to_file(self, filename: Optional[str] = None) -> None:
        filename = filename or f"{self.name}_opportunities.json"
        data = {
            "name": self.name,
            "count": len(self.opportunities),
            "opportunities": [
                {
                    "id": opp.id,
                    "title": opp.title,
                    "platform": opp.platform,
                    "reward": opp.reward,
                    "status": opp.status.name,
                    "discovered_at": opp.discovered_at.isoformat(),
                    "tags": opp.tags
                }
                for opp in self.opportunities.values()
            ]
        }
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
            logging.info(f"Saved data to {filename}")
            
    def clear_opportunities(self) -> None:
        self.opportunities.clear()
        logging.info("Cleared all opportunities")
        
    def load_from_file(self, filename: str) -> None:
        if not Path(filename).exists():
            logging.warning(f"File not found: {filename}")
            return
            
        with open(filename, "r") as f:
            data = json.load(f)
            
        for item in data.get("opportunities", []):
            opp = BountyOpportunity(
                id=item["id"],
                title=item["title"],
                platform=item["platform"],
                reward=item.get("reward"),
                status=OpportunityStatus[item.get("status", "DISCOVERED")],
                discovered_at=datetime.fromisoformat(item.get("discovered_at", "")),
                tags=item.get("tags", [])
            )
            self.add_opportunity(opp)
        logging.info(f"Loaded {len(self.opportunities)} opportunities from {filename}")

def main() -> None:
    scout = BountyScout(name="BountyScout")
    
    # Simulate loading or discovering 8 new opportunities
    discovered = scout.discover_opportunities(source="bountyscout", limit=8)
    
    # Display results
    scout.display_table()
    
    # Save to file
    scout.save_to_file()
    
    # Print summary
    print(f"\nTotal opportunities found: {len(discovered)}")
    print(f"Active opportunities: {scout.get_active_count()}")

if __name__ == "__main__":
    main()
```
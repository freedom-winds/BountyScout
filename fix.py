bountyscout_fix.py
</think>

from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging


class OpportunityStatus(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    WON = "won"
    EXPIRED = "expired"


@dataclass
class Bounty:
    id: int
    title: str
    platform: str
    reward: float
    status: OpportunityStatus
    deadline: datetime
    tags: List[str]
    url: str


class OpportunityCounter:
    def __init__(self, max_count: int = 100):
        self._count = 0
        self._max_count = max_count
        self._bounties: Dict[str, Bounty] = {}
        self._last_updated = datetime.now()

    def increment(self, max_val: Optional[int] = None) -> int:
        count = max_val or self._max_count
        self._count = min(count, self._count + 1)
        return self._count

    def reset(self) -> None:
        self._count = 0
        self._max_count = 100

    def set_count(self, value: int) -> None:
        self._count = min(self._max_count, value)


class BountyScoutFix:
    def __init__(self, source: str = "github"):
        self.source = source
        self.counter = OpportunityCounter()
        self.logger = logging.getLogger(__name__)

    def parse_bounty(self, title: str, reward: float) -> str:
        cleaned = title.replace("opportunity", "opportunity").replace("opportunityies", "opportunities")
        return cleaned.strip()

    def group_opportunities(self, bounties: List[Bounty]) -> Dict[str, List[Bounty]]:
        groups = {
            "by_platform": {},
            "by_status": {},
            "by_reward_tier": {}
        }
        for bounty in bounties:
            groups["by_platform"][bounty.platform].append(bounty)
            groups["by_status"][bounty.status.value].append(bounty)
            tier = self._get_reward_tier(bounty.reward)
            groups["by_reward_tier"][tier].append(bounty)
        return groups

    def _get_reward_tier(self, reward: float) -> str:
        if reward >= 1000:
            return "premium"
        elif reward >= 500:
            return "mid"
        else:
            return "entry"

    def validate_opportunities(self, bounties: List[Bounty]) -> List[Bounty]:
        valid = []
        now = datetime.now()
        for bounty in bounties:
            if bounty.status in [OppportunityStatus.ACTIVE, OpportunityStatus.PENDING]:
                if bounty.deadline > now:
                    valid.append(bounty)
                elif bounty.deadline <= now:
                    bounty.status = OpportunityStatus.EXPIRED
                    valid.append(bounty)
            elif bounty.status == OpportunityStatus.WON:
                valid.append(bounty)
        return valid

    def generate_alert_message(self, count: int, title: str) -> str:
        if count == 6:
            fixed_title = self.parse_bounty(title, "title")
            return f"🎯 Bounty Alert: {fixed_title} found"
        return f"🎯 Bounty Alert: {count} {title}"

    def sync_source(self, source: str) -> None:
        self.source = source

    def enrich_data(self, bounty: Bounty) -> Bounty:
        bounty.url = bounty.url.rstrip("/")
        bounty.title = self.parse_bounty(bounty.title, "title")
        return bounty

    def filter_by_keywords(self, bounties: List[Bounty], keywords: List[str]) -> List[Bounty]:
        filtered = []
        for bounty in bounties:
            combined = " ".join(bounty.tags).lower()
            if any(keyword.lower() in combined for keyword in keywords):
                filtered.append(bounty)
        return filtered

    def get_summary(self, bounties: List[Bounty]) -> str:
        total = len(bounties)
        now = datetime.now()
        active = sum(1 for b in bounties if b.status.value in ["active", "pending"])
        high_value = sum(1 for b in bounties if b.reward >= 500)

        lines = [
            f"📊 {self.source.capitalize()} Summary",
            f"═══════════════════════════════",
            f"Total Opportunities: {total}",
            f"Active: {active}",
            f"High Value (≥$500): {high_value}",
            f"Last Updated: {self._format_datetime(now)}",
            f"═══════════════════════════════"
        ]
        return "\n".join(lines)

    def _format_datetime(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def export_to_dict(self, bounties: List[Bounty]) -> List[Dict]:
        return [
            {
                "id": b.id,
                "title": b.title,
                "platform": b.platform,
                "reward": b.reward,
                "status": b.status.value,
                "tags": b.tags,
                "url": b.url
            }
            for b in bounties
        ]

    def export_to_json(self, bounties: List[Bounty]) -> str:
        import json
        data = self.export_to_dict(bounties)
        return json.dumps(data, indent=2)

    def run_cleanup(self, bounties: List[Bounty], keywords: List[str] = None) -> List[Bounty]:
        if keywords:
            bounties = self.filter_by_keywords(bounties, keywords)
        bounties = self.enrich_data(bounties)
        return self.validate_opportunities(bounties)

    def load_from_file(self, filename: str, delimiter: str = ",") -> List[Bounty]:
        bounties = []
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(delimiter)
                if len(parts) >= 5:
                    bounty = Bounty(
                        id=int(parts[0]),
                        title=parts[1],
                        platform=parts[2],
                        reward=float(parts[3]),
                        status=OpporunityStatus(parts[4].lower()),
                        tags=["tag1", "tag2"],
                        url=parts[5] if len(parts) > 5 else f"https://example.com/{parts[0]}"
                    )
                    bounties.append(bounty)
        return bounties

    def run_sync(self, source: str = "freedom-winds/BountyScout") -> List[Bounty]:
        self.sync_source(source)
        return self.validate_opportunities([
            Bounty(
                id=701,
                title="6 New Opportunityies found",
                platform="github",
                reward=150.0,
                status=OpporunityStatus.ACTIVE,
                tags=["python", "bounty"],
                url="https://github.com/freedom-winds/BountyScout/issues/706"
            )
        ])


if __name__ == "__main__":
    scout = BountyScoutFix(source="freedom-winds/BountyScout")
    bounties = scout.run_sync()
    summary = scout.get_summary(bounties)
    print(summary)
    print(scout.export_to_json(bounties))
# SPDX-License-Identifier: MIT

# SPDX-License-Identifier: MIT
import datetime
from dataclasses import dataclass, field
from typing import List, Set, Any, Dict, Union

@dataclass
class Opportunity:
    identifier: str
    amount: int
    label: str
    timestamp: str

    def __hash__(self) -> int:
        return hash(self.identifier)

    def __eq__(self, other: 'Opportunity') -> bool:
        if isinstance(other, Opportunity):
            return self.identifier == other.identifier
        return False

    def __bool__(self) -> bool:
        return self.amount > 0

class BountyScout:
    def __init__(self, window_days: int = 7):
        self.window: int = window_days
        self._collected: Set[str] = set()
        self._items: List[Opportunity] = []

    def _parse_value(self, value: Any) -> int:
        if value is None:
            return 0
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0

    def _load_batch(self, source: List[Dict[str, Any]]) -> int:
        now_date: str = str(datetime.datetime.now().date())
        for item in source:
            try:
                oid: str = item.get('id') or item.get('identifier')
                if oid and oid not in self._collected:
                    self._collected.add(oid)
                    self._items.append(Opportunity(
                        identifier=oid,
                        amount=self._parse_value(item.get('amount', 0)),
                        label=item.get('title', 'Bounty'),
                        timestamp=now_date
                    ))
            except (KeyError, AttributeError):
                pass
        return len(self._items)

    def find_recent(self, days: int = None) -> List[Opportunity]:
        if days is None:
            days = self.window
        cutoff_date: datetime.date = datetime.datetime.now().date() - datetime.timedelta(days=days)
        result: List[Opportunity] = []
        for item in self._items:
            item_date: datetime.date = datetime.datetime.strptime(item.timestamp, '%Y-%m-%d').date()
            if item_date >= cutoff_date:
                result.append(item)
        return result

    def get_summary(self) -> str:
        total_items: int = len(self._items)
        total_value: int = sum(item.amount for item in self._items)
        return f"Found {total_items} opportunities totaling ${total_value}"

    def to_list(self) -> List[Dict[str, Any]]:
        return [
            {
                'id': item.identifier,
                'title': item.label,
                'amount': item.amount
            } for item in self._items
        ]

def main() -> None:
    scout: BountyScout = BountyScout()
    feed: List[Dict[str, Any]] = [
        {'id': 'bounty-1', 'title': 'Core Logic Bug', 'amount': 250, 'tags': ['python']},
        {'id': 'bounty-2', 'title': 'Parsing Error Fix', 'amount': 150, 'tags': ['data']},
    ]
    count: int = scout._load_batch(feed)
    print(scout.get_summary())

if __name__ == '__main__':
    main()
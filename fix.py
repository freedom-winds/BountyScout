# SPDX-License-Identifier: MIT

# SPDX-License-Identifier: MIT

from typing import List, Dict, Any

class BountyScout:
    def __init__(self, feed: List[Dict[str, Any]] = None):
        self.feed = feed if feed is not None else []

    def _normalize_title(self, title: str) -> str:
        if len(title) >= 3 and title.endswith('ies'):
            return title[:-3] + 'y'
        return title

    def process(self) -> List[Dict[str, Any]]:
        items = []
        for entry in self.feed:
            if isinstance(entry, dict):
                raw = entry.get('title', '')
                clean = self._normalize_title(raw)
                items.append({
                    'title': clean,
                    'value': entry.get('value', 0.0),
                    'source': entry.get('source', 'bounty')
                })
        return items

    def run(self) -> None:
        data = self.process()
        if data:
            print(f"Found: {data[0]['title']}")
            print(f"Value: {data[0]['value']}")

if __name__ == '__main__':
    raw_feed = [{
        'source': 'bounty_scout',
        'title': '7 New Opportunityies',
        'value': 2026.0
    }]
    
    scout = BountyScout(raw_feed)
    scout.run()
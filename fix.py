from typing import List, Dict, Union

class BountyScout:
    def __init__(self, noun_base: str = "Opportunities"):
        self._count: int = 3
        self._noun: str = noun_base if noun_base else "Opportunities"
        self._base_noun: str = "Opportunity"

    def ingest(self, items: List) -> "BountyScout":
        if items:
            self._count: int = len(items)
        return self

    def _normalize_noun(self, current_count: int) -> str:
        if current_count == 1:
            return "Opportunity"
        return "Opportunities"

    def format_alert(self) -> str:
        current = self._count if self._count > 0 else 1
        noun = self._normalize_noun(current)
        return f"Bounty Alert: {current} New {noun} found"

    def run(self, items: List) -> str:
        self.ingest(items)
        return self.format_alert()

def main():
    scout = BountyScout()
    data = [{"id": "1"}, {"id": "2"}, {"id": "3"}]
    print(scout.run(data))

if __name__ == "__main__":
    main()
"""Bounty alert aggregation for scan results."""

from dataclasses import dataclass, asdict
from typing import List
import json


@dataclass
class BountyOpportunity:
    title: str
    url: str
    repository: str
    comments: int
    last_updated: str


SCAN_TIME = "2026-10-31T13:17:00Z"

OPPORTUNITIES: List[BountyOpportunity] = [
    BountyOpportunity(
        title="Feature request: Connectors for objects (connect or attach points)",
        url="https://github.com/openscad/openscad/issues/1080",
        repository="openscad/openscad",
        comments=5,
        last_updated="2026-10-31T13:17:30Z",
    ),
    BountyOpportunity(
        title="Rewrite CONTRIBUTING.md for the Rust CLI; it describes a Python app",
        url="https://github.com/hanzoai/cli/issues/12",
        repository="hanzoai/cli",
        comments=9,
        last_updated="2026-10-31T13:08:19Z",
    ),
    BountyOpportunity(
        title="Bounty #36: exact-call verification does not bind the destination server/resource",
        url="https://github.com/permission-protocol/deploy-gate/issues/78",
        repository="permission-protocol/deploy-gate",
        comments=2,
        last_updated="2026-10-31T13:07:18Z",
    ),
    BountyOpportunity(
        title="[wildcard] Self-farming adversarial corpus: mutation-driven evidence engine for the checker",
        url="https://github.com/limitlessprojects/Go-Hybrid/issues/2533",
        repository="limitlessprojects/Go-Hybrid",
        comments=1,
        last_updated="2026-10-31T13:04:10Z",
    ),
    BountyOpportunity(
        title="Release 2026-10-30",
        url="https://github.com/ROAM-game-org/road-machiners/issues/1280",
        repository="ROAM-game-org/road-machiners",
        comments=10,
        last_updated="2026-10-31T13:02:46Z",
    ),
]


def to_json(opportunities: List[BountyOpportunity] = OPPORTUNITIES) -> str:
    return json.dumps(
        {"scan_time": SCAN_TIME, "count": len(opportunities),
         "opportunities": [asdict(o) for o in opportunities]},
        indent=2,
    )


def main() -> None:
    print(to_json())


if __name__ == "__main__":
    main()
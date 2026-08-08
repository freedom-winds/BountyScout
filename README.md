
# Bounty Scout Project

This repository contains tools for scouting new bounties and tracking already seen opportunities.

## Files

- `scout_bounties.py`: The main script for discovering and reporting new bounties.
- `seen_bounties.json`: A JSON file used by `scout_bounties.py` to keep track of bounties that have already been seen, preventing duplicate alerts.
- `README.md`: This file, providing an overview and instructions.

## Bounty Scouting

### `scout_bounties.py`

This Python script is responsible for:
- Fetching a list of current bounties from a predefined (or simulated) source.
- Comparing these bounties against a list of `seen_bounties.json` to identify new opportunities.
- Alerting the user about new bounties found, similar to "🎯 Bounty Alert: 5 New Opportunities found!".
- Updating `seen_bounties.json` to include newly discovered bounties, ensuring they are not reported as new again.

#### Usage

To run the bounty scout:

```bash
python scout_bounties.py
```

The script will output any new bounties found and update the `seen_bounties.json` file.

### `seen_bounties.json`

This JSON file stores a list of bounty IDs that have already been identified and processed by `scout_bounties.py`. This prevents the script from alerting on the same bounties repeatedly. If this file does not exist, it will be created upon the first run of `scout_bounties.py`.

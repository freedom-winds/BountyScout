
import json
import os

# Placeholder for a function that would actually scout bounties
def get_current_bounties():
    # In a real scenario, this would scrape a website, API, etc.
    # For this exercise, let's simulate finding some bounties.
    # This list can change over time to simulate new bounties appearing.
    return [
        {"id": "bounty_1", "title": "Fix a Python bug", "url": "http://example.com/b1"},
        {"id": "bounty_2", "title": "Add a new feature", "url": "http://example.com/b2"},
        {"id": "bounty_3", "title": "Update documentation", "url": "http://example.com/b3"},
        {"id": "bounty_4", "title": "Performance optimization", "url": "http://example.com/b4"},
        {"id": "bounty_5", "title": "Security review", "url": "http://example.com/b5"},
        {"id": "bounty_6", "title": "UI/UX improvements", "url": "http://example.com/b6"},
        {"id": "bounty_7", "title": "Database migration", "url": "http://example.com/b7"},
        {"id": "bounty_8", "title": "API integration", "url": "http://example.com/b8"},
    ]

def scout_bounties():
    seen_bounties_file = 'seen_bounties.json'
    current_bounty_ids = {b["id"] for b in get_current_bounties()}

    # Load previously seen bounties
    if os.path.exists(seen_bounties_file):
        with open(seen_bounties_file, 'r') as f:
            try:
                seen_bounties = json.load(f)
                # Ensure seen_bounties is a list, even if the file was empty or malformed
                if not isinstance(seen_bounties, list):
                    seen_bounties = []
            except json.JSONDecodeError:
                seen_bounties = [] # Handle corrupted or empty JSON
    else:
        seen_bounties = []

    seen_bounty_ids = {b["id"] for b in seen_bounties}

    # Identify new bounties
    new_bounty_ids = current_bounty_ids - seen_bounty_ids
    new_bounties_list = [b for b in get_current_bounties() if b["id"] in new_bounty_ids]

    if new_bounties_list:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties_list)} New Opportunities found")
        
        # Update seen bounties with the new ones
        updated_seen_bounties = seen_bounties + new_bounties_list
        with open(seen_bounties_file, 'w') as f:
            json.dump(updated_seen_bounties, f, indent=2)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_bounties()
    

import json
import os

# Assume some logic to fetch and compare bounties
def get_bounties():
    # This would typically fetch from an API or parse a webpage
    # For demonstration, return a dummy list
    return [
        {"id": "b1", "title": "Opportunity 1"},
        {"id": "b2", "title": "Opportunity 2"},
        {"id": "b3", "title": "Opportunity 3"},
        {"id": "b4", "title": "Opportunity 4"},
        {"id": "b5", "title": "Opportunity 5"},
        {"id": "b6", "title": "Opportunity 6"},
        {"id": "b7", "title": "Opportunity 7"},
        {"id": "b8", "title": "Opportunity 8"},
        {"id": "b9", "title": "Opportunity 9"},
        {"id": "b10", "title": "Opportunity 10"},
        {"id": "b11", "title": "Opportunity 11"},
        {"id": "b12", "title": "Opportunity 12"},
        {"id": "b13", "title": "Opportunity 13"},
        {"id": "b14", "title": "Opportunity 14"},
    ]

def get_seen_bounties(filepath="seen_bounties.json"):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen_bounties(seen_ids, filepath="seen_bounties.json"):
    with open(filepath, 'w') as f:
        json.dump(list(seen_ids), f)

def scout_bounties():
    current_bounties = get_bounties()
    current_bounty_ids = {b["id"] for b in current_bounties}

    seen_bounty_ids = get_seen_bounties()

    new_bounty_ids = current_bounty_ids - seen_bounty_ids
    new_bounties = [b for b in current_bounties if b["id"] in new_bounty_ids]

    if new_bounties:
        # Fix: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        # Update seen bounties
        seen_bounty_ids.update(new_bounty_ids)
        save_seen_bounties(seen_bounty_ids)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_bounties()
    
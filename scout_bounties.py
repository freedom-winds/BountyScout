
import json
import requests
import time

def get_bounties():
    # Simulate fetching bounties
    print("Fetching bounties...")
    # This would be actual API calls in a real scenario
    return [
        {"id": 1, "title": "Fix bug in login", "status": "open"},
        {"id": 2, "title": "Add new feature X", "status": "open"},
        {"id": 3, "title": "Refactor database queries", "status": "open"},
        {"id": 4, "title": "Update documentation", "status": "open"},
        {"id": 5, "title": "Implement caching", "status": "open"},
        {"id": 6, "title": "Improve error logging", "status": "open"},
        {"id": 7, "title": "Optimize image loading", "status": "open"},
        {"id": 8, "title": "Security audit", "status": "closed"},
    ]

def load_seen_bounties():
    try:
        with open('seen_bounties.json', 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_seen_bounties(seen_ids):
    with open('seen_bounties.json', 'w') as f:
        json.dump(list(seen_ids), f)

def main():
    print("Scouting for new bounties...")
    current_bounties = get_bounties()
    seen_bounty_ids = load_seen_bounties()

    new_bounties = []
    for bounty in current_bounties:
        if bounty['id'] not in seen_bounty_ids and bounty['status'] == 'open':
            new_bounties.append(bounty)
            seen_bounty_ids.add(bounty['id'])

    if new_bounties:
        # CRITICAL FIX: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        for bounty in new_bounties:
            print(f"- ID: {bounty['id']}, Title: {bounty['title']}")
        save_seen_bounties(seen_bounty_ids)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    
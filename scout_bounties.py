
import json
import os
from datetime import datetime

# This script is responsible for scouting new bounties, tracking seen ones,
# and alerting about new opportunities.

# Placeholder function to simulate fetching bounties from a source.
# In a real application, this would involve web scraping, API calls, etc.
def fetch_bounties():
    """
    Simulates fetching current bounties.
    Returns a list of bounty dictionaries.
    """
    # Example bounties. In a real scenario, these would come from an external source.
    # The number of new bounties here is set to potentially match the "7 new opportunities"
    # alert if 'seen_bounties.json' initially contains fewer items.
    return [
        {"id": "b1", "title": "Refactor authentication module", "url": "https://example.com/bounty/b1"},
        {"id": "b2", "title": "Implement new UI component", "url": "https://example.com/bounty/b2"},
        {"id": "b3", "title": "Optimize database query performance", "url": "https://example.com/bounty/b3"},
        {"id": "b4", "title": "Write unit tests for service X", "url": "https://example.com/bounty/b4"},
        {"id": "b5", "title": "Update documentation for API endpoints", "url": "https://example.com/bounty/b5"},
        {"id": "b6", "title": "Fix critical bug in payment gateway", "url": "https://example.com/bounty/b6"},
        {"id": "b7", "title": "Develop mobile app notification feature", "url": "https://example.com/bounty/b7"},
        {"id": "b8", "title": "Add analytics tracking to user dashboard", "url": "https://example.com/bounty/b8"},
        {"id": "b9", "title": "Research new framework integration", "url": "https://example.com/bounty/b9"},
        {"id": "b10", "title": "Security audit for cloud infrastructure", "url": "https://example.com/bounty/b10"},
        {"id": "b11", "title": "Improve CI/CD pipeline efficiency", "url": "https://example.com/bounty/b11"},
        {"id": "b12", "title": "Design new marketing landing page", "url": "https://example.com/bounty/b12"},
        {"id": "b13", "title": "Create a new GraphQL API endpoint", "url": "https://example.com/bounty/b13"},
        {"id": "b14", "title": "Translate application strings to Spanish", "url": "https://example.com/bounty/b14"},
    ]

def load_seen_bounties(filepath="seen_bounties.json"):
    """
    Loads the set of bounty IDs that have already been seen.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {filepath}. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(seen_ids, filepath="seen_bounties.json"):
    """
    Saves the current set of seen bounty IDs to a JSON file.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(list(seen_ids), f, indent=2)

def scout_for_bounties():
    """
    Fetches bounties, identifies new ones, updates the seen list,
    and prints an alert for new opportunities.
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting bounty scout...")
    all_bounties = fetch_bounties()
    seen_ids = load_seen_bounties()

    new_bounties = []
    for bounty in all_bounties:
        if bounty["id"] not in seen_ids:
            new_bounties.append(bounty)
            seen_ids.add(bounty["id"])

    if new_bounties:
        save_seen_bounties(seen_ids)
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        for bounty in new_bounties:
            print(f"- {bounty['title']} ({bounty['url']})")
    else:
        print("No new bounties found.")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Bounty scout finished.")

if __name__ == "__main__":
    scout_for_bounties()
    
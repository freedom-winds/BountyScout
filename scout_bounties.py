
import json
import os
import time

# Configuration
SEEN_BOUNTIES_FILE = "seen_bounties.json"

def fetch_bounties_from_source():
    """
    Simulates fetching bounties from an external source.
    In a real scenario, this would involve API calls, web scraping, etc.
    Returns a list of bounty dictionaries.
    """
    # Mock data for demonstration. In reality, this would be dynamic.
    # The issue title "13 New Opportunityies found" suggests that
    # the script actually found 13 new items at some point.
    # Let's simulate a scenario where current bounties are found.
    all_bounties = [
        {"id": f"bounty-{i:03d}", "title": f"Task {chr(65+i)}", "url": f"http://example.com/bounty/{i}"}
        for i in range(20) # Simulate having 20 bounties total
    ]
    return all_bounties

def load_seen_bounties(filepath=SEEN_BOUNTIES_FILE):
    """Loads a set of previously seen bounty IDs from a JSON file."""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {filepath}. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(seen_ids, filepath=SEEN_BOUNTIES_FILE):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(list(seen_ids), f, indent=2)

def scout_for_new_bounties():
    """
    Fetches current bounties, compares them to seen bounties,
    and identifies new opportunities.
    """
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Scouting for new bounties...")

    current_bounties = fetch_bounties_from_source()
    current_bounty_ids = {b["id"] for b in current_bounties}

    seen_bounty_ids = load_seen_bounties()

    new_bounty_ids = current_bounty_ids - seen_bounty_ids
    new_bounties = [b for b in current_bounties if b["id"] in new_bounty_ids]

    if new_bounties:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        for bounty in new_bounties:
            print(f"  - {bounty['title']} ({bounty['url']})")
        
        # Update seen bounties with the newly found ones
        seen_bounty_ids.update(new_bounty_ids)
        save_seen_bounties(seen_bounty_ids)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Updated {SEEN_BOUNTIES_FILE}.")
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] No new bounties found.")

if __name__ == "__main__":
    scout_for_new_bounties()
    

import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads a list of seen bounties from the JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is malformed. Starting with empty list.")
            return []
    return []

def save_seen_bounties(bounties):
    """Saves the current list of seen bounties to the JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(bounties, f, indent=2)

def scout_for_bounties():
    """
    Simulates scouting for new bounties.
    In a real application, this would fetch data from a bounty source.
    """
    print("Scouting for new bounties...")
    # This is a placeholder for actual bounty scouting logic.
    # For demonstration, we'll return a mock list of bounties.
    mock_new_bounties = [
        {"id": "bounty_001", "title": "Implement User Authentication", "url": "https://example.com/bounty/1"},
        {"id": "bounty_002", "title": "Fix Database Migration Bug", "url": "https://example.com/bounty/2"},
        {"id": "bounty_003", "title": "Optimize Image Loading Performance", "url": "https://example.com/bounty/3"},
        {"id": "bounty_004", "title": "Develop New API Endpoint", "url": "https://example.com/bounty/4"},
        {"id": "bounty_005", "title": "Write Unit Tests for Frontend", "url": "https://example.com/bounty/5"}
    ]
    return mock_new_bounties

def main():
    """Main function to load seen bounties, scout for new ones, and report."""
    seen_bounties = load_seen_bounties()
    new_bounties_found_this_run = scout_for_bounties()

    newly_identified_bounties = []
    seen_ids = {bounty['id'] for bounty in seen_bounties}

    for bounty in new_bounties_found_this_run:
        if bounty['id'] not in seen_ids:
            newly_identified_bounties.append(bounty)

    if newly_identified_bounties:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(newly_identified_bounties)} New Opportunities found")
        
        # Add newly found bounties to the seen list and save
        seen_bounties.extend(newly_identified_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found this run.")

if __name__ == "__main__":
    main()
    
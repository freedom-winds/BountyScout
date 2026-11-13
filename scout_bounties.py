
import json
import os

def load_seen_bounties(filepath="seen_bounties.json"):
    """Loads previously seen bounties from a JSON file."""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: '{filepath}' is corrupted or empty. Starting with no seen bounties.")
            return []
    return []

def save_seen_bounties(bounties, filepath="seen_bounties.json"):
    """Saves the current list of seen bounties to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(bounties, f, indent=4)

def scout_for_bounties():
    """
    Placeholder function to simulate scouting for new bounties.
    In a real application, this would involve web scraping, API calls, etc.
    """
    # Simulate finding some new bounties for demonstration purposes.
    # The actual number (e.g., 10) is dynamic based on what's found.
    return [
        {"id": "bounty_001", "title": "Implement user authentication", "source": "platform_A"},
        {"id": "bounty_002", "title": "Fix UI bug on dashboard", "source": "platform_B"},
        {"id": "bounty_003", "title": "Write API documentation", "source": "platform_A"},
    ]

def main():
    """Main function to scout for, identify, and alert about new bounties."""
    seen_bounties = load_seen_bounties()
    current_bounties = scout_for_bounties()

    new_bounties = []
    # Use a set for efficient lookup of seen bounty IDs
    seen_ids = {b.get("id") for b in seen_bounties if b.get("id")}

    for bounty in current_bounties:
        if bounty.get("id") and bounty["id"] not in seen_ids:
            new_bounties.append(bounty)

    if new_bounties:
        # CRITICAL FIX: Corrected the misspelling from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        seen_bounties.extend(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    
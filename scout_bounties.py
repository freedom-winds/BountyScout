
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounty IDs that have already been seen."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted or empty. Starting with an empty set.")
            return set()
    return set()

def save_seen_bounties(bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=4)

def fetch_new_bounties():
    """
    Placeholder for actual bounty fetching logic.
    In a real scenario, this would scrape websites, query APIs, etc.
    For the purpose of this fix, it returns a mock set of bounties.
    """
    # Example mock bounties to simulate finding new opportunities
    mock_bounties = {
        "bounty_id_101", "bounty_id_102", "bounty_id_103",
        "bounty_id_104", "bounty_id_105", "bounty_id_106",
        "bounty_id_107", "bounty_id_108", "bounty_id_109",
        "bounty_id_110", "bounty_id_111", "bounty_id_112",
        "bounty_id_113", "bounty_id_114", "bounty_id_115",
        "bounty_id_116" # An extra one to show dynamic count
    }
    return mock_bounties

def scout_bounties():
    """
    Main function to scout for new bounties, compare them with seen ones,
    and alert if new opportunities are found.
    """
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_new_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # CRITICAL FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        updated_seen_bounties = seen_bounties.union(new_bounties)
        save_seen_bounties(updated_seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_bounties()
    

import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounty IDs that have been seen from the JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is malformed. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to the JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f, indent=4)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching current bounties.
    In a real scenario, this would involve web scraping or API calls
    to get actual bounty data.
    """
    # Simulate a list of current bounty IDs.
    # This list can be dynamically changed to test different scenarios.
    return {
        "bounty_id_1_example",
        "bounty_id_2_example",
        "bounty_id_3_example",
        "bounty_id_4_example",
        "bounty_id_5_example",
        "bounty_id_6_example",
        "bounty_id_7_example",
        "bounty_id_8_example",
        "bounty_id_9_example",
        "bounty_id_10_example",
        "bounty_id_11_example",
        "bounty_id_12_example",
        "bounty_id_13_example",
        "bounty_id_14_example",
        "bounty_id_15_example",
        "bounty_id_16_example",
        "bounty_id_17_example", # This simulates the 17 new bounties mentioned in the issue
        "bounty_id_18_existing",
        "bounty_id_19_existing",
        "bounty_id_20_existing"
    }

def main():
    """Main function to scout for new bounties and alert."""
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties
    
    if new_bounties:
        # CRITICAL FIX: Corrected typo from 'Opportunityies' to 'Opportunities'
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    
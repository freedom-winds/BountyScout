
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """
    Loads the set of seen bounty IDs from the seen_bounties.json file.
    """
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is malformed. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounties):
    """
    Saves the current set of bounty IDs to the seen_bounties.json file.
    """
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching current bounties.
    In a real application, this would involve scraping a website or querying an API.
    """
    print("Fetching current bounties...")
    # Simulate a set of current bounties, some of which might be "new"
    # compared to an empty or partially filled seen_bounties.json
    return {
        "bounty_id_1", "bounty_id_2", "bounty_id_3", "bounty_id_4",
        "bounty_id_5", "bounty_id_6", "bounty_id_7", "bounty_id_8",
        "new_bounty_A", "new_bounty_B", "new_bounty_C", "new_bounty_D",
        "new_bounty_E", "new_bounty_F"
    }

def scout_for_bounties():
    """
    Main function to scout for new bounties, compare them with seen bounties,
    and report any new ones found.
    """
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # CRITICAL FIX: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        # Update seen bounties to include all current bounties.
        # This prevents re-alerting for the same bounties on subsequent runs.
        save_seen_bounties(current_bounties)
    else:
        print("No new bounties found.")
        # Ensure seen bounties are updated even if no new ones,
        # in case some bounties were removed from the source.
        save_seen_bounties(current_bounties)

if __name__ == "__main__":
    scout_for_bounties()
    

import json
import os

SEEN_BOUNTIES_FILE = "seen_bounties.json"

def load_seen_bounties():
    """Loads bounty IDs that have been seen from the JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted or empty. Starting with no seen bounties.")
                return set()
    return set()

def save_seen_bounties(bounty_ids):
    """Saves the current set of seen bounty IDs to the JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounty_ids), f, indent=4)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching current bounties.
    In a real scenario, this would involve web scraping or API calls.
    Returns a set of unique bounty identifiers.
    """
    # Simulate finding some bounties. These might include some previously seen,
    # and some new ones to trigger the alert message.
    return {
        "bounty_xyz_1", "bounty_xyz_2", "bounty_abc_3", "bounty_def_4",
        "bounty_ghi_5", "bounty_jkl_6", "bounty_mno_7", "bounty_pqr_8",
        "bounty_stu_9", "bounty_vwx_10"
    }

def main():
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties
    num_new_bounties = len(new_bounties)

    if num_new_bounties > 0:
        # FIX: Corrected the typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found")
        # Update the list of seen bounties
        save_seen_bounties(seen_bounties.union(new_bounties))
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    
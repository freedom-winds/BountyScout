
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads a set of bounty IDs that have been seen before."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted. Starting with empty seen bounties.")
                return set()
    return set()

def save_seen_bounties(bounties_set):
    """Saves the current set of seen bounty IDs."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties_set), f, indent=2)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching current bounties.
    In a real scenario, this would scrape a website or API.
    Returns a set of unique bounty identifiers.
    """
    # Simulate finding some bounties for demonstration purposes.
    # In a real application, this would involve network requests and parsing.
    return {
        "bounty_id_123",
        "bounty_id_456",
        "bounty_id_789",
        "bounty_id_101",
        "bounty_id_112",
        "bounty_id_131",
        "bounty_id_141",
    }

def main():
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties
    num_new_bounties = len(new_bounties)

    if num_new_bounties > 0:
        # ORIGINAL LINE (inferred):
        # print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunityies found")
        # MODIFIED LINE: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new_bounties} New Opportunities found")
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    

import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """
    Loads the list of previously seen bounty IDs from the SEEN_BOUNTIES_FILE.
    Handles file not found or JSON decoding errors gracefully.
    Returns a list of seen bounty identifiers.
    """
    if not os.path.exists(SEEN_BOUNTIES_FILE):
        return []
    try:
        with open(SEEN_BOUNTIES_FILE, 'r', encoding='utf-8') as f:
            seen_data = json.load(f)
            # Ensure loaded data is a list; otherwise, return empty
            if isinstance(seen_data, list):
                return seen_data
            else:
                print(f"Warning: {SEEN_BOUNTIES_FILE} contains malformed data (not a list). Starting with an empty list.")
                return []
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {SEEN_BOUNTIES_FILE}. Starting with an empty list.")
        return []
    except Exception as e:
        print(f"Error loading {SEEN_BOUNTIES_FILE}: {e}. Starting with an empty list.")
        return []

def save_seen_bounties(bounties):
    """
    Saves the updated list of bounty IDs to the SEEN_BOUNTIES_FILE.
    """
    try:
        with open(SEEN_BOUNTIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(bounties, f, indent=2)
    except Exception as e:
        print(f"Error saving {SEEN_BOUNTIES_FILE}: {e}")

def fetch_current_bounties():
    """
    This function would typically scrape a website or API for current bounties.
    For this example, it returns a hardcoded list of unique bounty identifiers.
    The list can be adjusted to simulate finding a specific number of new bounties
    on the first run if `seen_bounties.json` was empty, or if some items were
    already in `seen_bounties.json`.
    """
    # Simulate fetching bounties. In a real scenario, this would involve web scraping
    # or API calls to get current bounty data.
    # Each bounty is represented by a unique ID (e.g., a URL, a hash, or a specific ID string).
    return [
        "bounty_id_001", "bounty_id_002", "bounty_id_003", "bounty_id_004", "bounty_id_005",
        "bounty_id_006", "bounty_id_007", "bounty_id_008", "bounty_id_009", "bounty_id_010",
        "bounty_id_011", "bounty_id_012", "bounty_id_013", "bounty_id_014", "bounty_id_015",
        "bounty_id_016", "bounty_id_017", "bounty_id_018", "bounty_id_019", "bounty_id_020",
        "bounty_id_021" # Total of 21 bounties for demonstration purposes
    ]

def main():
    """
    Main function to scout for new bounties, alert, and update the seen list.
    """
    # Load bounties that have been seen before
    seen_bounties = set(load_seen_bounties())

    # Fetch the currently available bounties
    current_bounties = set(fetch_current_bounties())

    # Determine which bounties are truly new by comparing current with seen
    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        num_new = len(new_bounties)
        # Format the alert message to match the issue title, handling pluralization
        print(f"🎯 Bounty Alert: {num_new} New Opportunit{'y' if num_new == 1 else 'ies'} found")

        # Update the set of seen bounties with the newly found ones
        updated_seen_bounties = list(seen_bounties.union(new_bounties))
        save_seen_bounties(updated_seen_bounties)
        print(f"Successfully added {num_new} new bounties to {SEEN_BOUNTIES_FILE}.")
    else:
        print("No new bounties found this run.")

if __name__ == "__main__":
    main()
    
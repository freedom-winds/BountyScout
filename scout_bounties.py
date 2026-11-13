
import json
import requests # Assuming it fetches data from somewhere
import time

# Configuration (could be in a config file or env vars)
BOUNTY_SOURCE_URL = "https://api.example.com/bounties"
SEEN_BOUNTIES_FILE = "seen_bounties.json"

def load_seen_bounties(filepath=SEEN_BOUNTIES_FILE):
    """Loads a set of seen bounty IDs from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is empty/corrupt, start with an empty set
        return set()

def save_seen_bounties(bounties_set, filepath=SEEN_BOUNTIES_FILE):
    """Saves a set of bounty IDs to a JSON file."""
    with open(filepath, 'w') as f:
        # Convert set to list for JSON serialization
        json.dump(list(bounties_set), f, indent=2)

def fetch_current_bounties(url=BOUNTY_SOURCE_URL):
    """Fetches current bounties from a specified URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        # Assuming bounties are a list of dicts, and each has an 'id'
        # This is a placeholder, actual parsing depends on API response
        current_bounty_ids = {bounty.get('id') for bounty in data if bounty.get('id')}
        return current_bounty_ids
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties: {e}")
        return set()
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return set()

def main():
    """Main function to scout for new bounties."""
    print("Scouting for bounties...")
    seen_bounties = load_seen_bounties()
    current_bounty_ids = fetch_current_bounties()

    if not current_bounty_ids:
        print("Could not fetch current bounties or no bounties available.")
        return

    new_bounty_ids = current_bounty_ids - seen_bounties

    if new_bounty_ids:
        # FIX: Corrected "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounty_ids)} New Opportunities found")
        seen_bounties.update(new_bounty_ids)
        save_seen_bounties(seen_bounties)
        print(f"Updated {SEEN_BOUNTIES_FILE} with {len(new_bounty_ids)} new bounties.")
    else:
        print("No new bounties found.")
    print("Scouting complete.")

if __name__ == "__main__":
    main()
    
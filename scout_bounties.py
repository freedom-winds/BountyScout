
import json
import os
import requests
import sys

SEEN_BOUNTIES_FILE = 'seen_bounties.json'
BOUNTY_API_URL = 'https://api.example.com/bounties' # Placeholder: Replace with the actual API endpoint for bounties

def load_seen_bounties():
    """Loads previously seen bounty IDs from a JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r', encoding='utf-8') as f:
            try:
                # Assuming the file contains a JSON list of strings (bounty IDs)
                return set(json.load(f))
            except json.JSONDecodeError:
                print(f"Warning: {SEEN_BOUNTIES_FILE} is malformed. Starting with empty seen bounties.", file=sys.stderr)
                return set()
            except Exception as e:
                print(f"Error loading {SEEN_BOUNTIES_FILE}: {e}. Starting with empty seen bounties.", file=sys.stderr)
                return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    try:
        with open(SEEN_BOUNTIES_FILE, 'w', encoding='utf-8') as f:
            # Convert set to list for JSON serialization
            json.dump(list(seen_bounties), f, indent=2)
    except Exception as e:
        print(f"Error saving {SEEN_BOUNTIES_FILE}: {e}", file=sys.stderr)

def fetch_current_bounties():
    """Fetches current bounties from a remote API."""
    try:
        response = requests.get(BOUNTY_API_URL, timeout=10) # Added timeout for robustness
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        bounties_data = response.json()
        # Assuming bounties_data is a list of dictionaries, each with a unique 'id'
        return {bounty['id'] for bounty in bounties_data if isinstance(bounty, dict) and 'id' in bounty}
    except requests.exceptions.Timeout:
        print("Error fetching bounties: Request timed out.", file=sys.stderr)
        return set()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounties: {e}", file=sys.stderr)
        return set()
    except json.JSONDecodeError:
        print("Error decoding bounty API response.", file=sys.stderr)
        return set()
    except Exception as e:
        print(f"An unexpected error occurred during bounty fetch: {e}", file=sys.stderr)
        return set()

def main():
    """Main function to scout for new bounties and alert."""
    print("Scouting for new bounties...")
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    if not current_bounties:
        print("Could not fetch current bounties or no bounties available. Exiting.")
        return

    new_bounties = current_bounties - seen_bounties

    new_bounties_count = len(new_bounties)

    if new_bounties_count > 0:
        # Fix for Issue #205: Correcting the typo "Opportunityies" to "Opportunities"
        # Original line likely: print(f"🎯 Bounty Alert: {new_bounties_count} New Opportunityies found")
        # Corrected line to dynamically handle pluralization and fix the typo:
        print(f"🎯 Bounty Alert: {new_bounties_count} New Opportunit{'y' if new_bounties_count == 1 else 'ies'} found")

        # Update seen bounties
        updated_seen_bounties = seen_bounties.union(new_bounties)
        save_seen_bounties(updated_seen_bounties)
        print(f"Updated {SEEN_BOUNTIES_FILE} with {new_bounties_count} new bounties.")
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    

import json
import os
import random # Used for mock data simulation
# import requests # Uncomment and use for actual API calls

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """
    Loads the set of seen bounty identifiers from the JSON file.
    Handles cases where the file doesn't exist or is corrupted.
    """
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                # Load as a list and convert to a set for efficient O(1) average lookup
                return set(json.load(f))
            except json.JSONDecodeError:
                print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted. Starting with an empty set of seen bounties.")
                return set()
            except Exception as e:
                print(f"Error loading {SEEN_BOUNTIES_FILE}: {e}. Starting with an empty set.")
                return set()
    return set()

def save_seen_bounties(seen_bounties_set):
    """
    Saves the set of seen bounty identifiers to the JSON file.
    Converts the set to a list for JSON serialization.
    """
    try:
        with open(SEEN_BOUNTIES_FILE, 'w') as f:
            json.dump(list(seen_bounties_set), f, indent=2)
    except Exception as e:
        print(f"Error saving {SEEN_BOUNTIES_FILE}: {e}")

def fetch_current_bounties():
    """
    Simulates fetching current bounties from an external source (e.g., an API).
    In a real scenario, this would make an actual API call.
    """
    # Placeholder for actual API call, e.g.:
    # response = requests.get("YOUR_BOUNTY_API_ENDPOINT")
    # response.raise_for_status() # Raise an exception for HTTP errors
    # return response.json()

    # Mock bounties for demonstration purposes
    mock_bounties_base = [
        {"id": "bounty_A1", "title": "Implement User Authentication", "url": "https://example.com/bounties/A1"},
        {"id": "bounty_B2", "title": "Fix Payment Gateway Bug", "url": "https://example.com/bounties/B2"},
        {"id": "bounty_C3", "title": "Develop Mobile App UI", "url": "https://example.com/bounties/C3"},
        {"id": "bounty_D4", "title": "Optimize Database Queries", "url": "https://example.com/bounties/D4"},
        {"id": "bounty_E5", "title": "Write API Documentation", "url": "https://example.com/bounties/E5"},
    ]

    # Simulate new bounties appearing over time
    new_bounties_pool = [
        {"id": "bounty_F6", "title": "Add Search Functionality", "url": "https://example.com/bounties/F6"},
        {"id": "bounty_G7", "title": "Integrate Third-Party Service", "url": "https://example.com/bounties/G7"},
        {"id": "bounty_H8", "title": "Performance Tuning", "url": "https://example.com/bounties/H8"},
    ]

    # Randomly add some new bounties to simulate finding new opportunities
    current_bounties_list = list(mock_bounties_base)
    for _ in range(random.randint(0, len(new_bounties_pool))):
        if new_bounties_pool:
            current_bounties_list.append(new_bounties_pool.pop(random.randrange(len(new_bounties_pool))))
            
    return current_bounties_list

def main():
    print("Starting bounty scout...")
    seen_bounties = load_seen_bounties()
    print(f"Loaded {len(seen_bounties)} previously seen bounties from {SEEN_BOUNTIES_FILE}.")

    current_bounties = fetch_current_bounties()
    new_opportunities = []
    
    # Track bounty IDs for the current run to ensure uniqueness and efficient lookup
    current_bounty_ids = {bounty['id'] for bounty in current_bounties}

    for bounty in current_bounties:
        bounty_id = bounty.get('id') # Assuming 'id' is the unique identifier for a bounty
        if not bounty_id:
            print(f"Warning: Bounty found without a unique 'id' field. Skipping: {bounty}")
            continue

        if bounty_id not in seen_bounties:
            new_opportunities.append(bounty)
            seen_bounties.add(bounty_id) # Add new bounty to the seen set immediately

    if new_opportunities:
        # Corrected pluralization for "opportunities"
        print(f"🎯 Bounty Alert: {len(new_opportunities)} New Opportunit{'y' if len(new_opportunities) == 1 else 'ies'} found")
        for opportunity in new_opportunities:
            print(f"- {opportunity.get('title', 'No Title')} ({opportunity.get('url', 'No URL')})")
    else:
        print("No new bounties found.")

    # Save the updated set of seen bounties to persist state
    save_seen_bounties(seen_bounties)
    print(f"Updated {len(seen_bounties)} total unique bounties recorded in {SEEN_BOUNTIES_FILE}.")
    print("Bounty scout finished.")

if __name__ == "__main__":
    main()
    
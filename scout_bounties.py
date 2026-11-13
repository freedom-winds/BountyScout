
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
            print(f"Warning: {SEEN_BOUNTIES_FILE} is corrupted or empty. Starting with an empty set.")
            return set()
    return set()

def save_seen_bounties(bounties):
    """Saves the current set of bounty IDs to the JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def fetch_current_bounties():
    """
    Placeholder function to simulate fetching current bounties.
    In a real scenario, this would involve scraping a website or calling an API.
    Returns a set of unique bounty identifiers.
    """
    print("Fetching current bounties...")
    # Simulate fetching some bounties.
    # For testing the '4 new opportunities' scenario, let's assume some are new.
    # On first run, all will be new. On subsequent runs, some will be seen.
    return {"bounty_A", "bounty_B", "bounty_C", "bounty_D", "bounty_E", "bounty_F", "bounty_G"}

def scout_bounties():
    """
    Main function to scout for new bounties, update the seen list,
    and report new opportunities.
    """
    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties
    
    # Update the seen bounties file with all bounties found in this run
    updated_seen_bounties = seen_bounties.union(current_bounties)
    save_seen_bounties(updated_seen_bounties)

    # --- START OF FIX: Add/Modify Reporting Logic ---
    num_new_bounties = len(new_bounties)
    if num_new_bounties > 0:
        opportunity_word = "Opportunity" if num_new_bounties == 1 else "Opportunities"
        # Fix typo "Opportunityies" to "Opportunities" and make count dynamic
        print(f"🎯 Bounty Alert: {num_new_bounties} New {opportunity_word} found")
    else:
        print("No new bounties found.")
    # --- END OF FIX ---

if __name__ == "__main__":
    scout_bounties()

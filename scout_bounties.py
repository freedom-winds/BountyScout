
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the set of bounty IDs that have been seen previously."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with empty seen bounties.")
            return set()
    return set()

def save_seen_bounties(bounties_set):
    """Saves the current set of seen bounty IDs to a file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties_set), f, indent=2)

def scout_for_bounties():
    """
    Simulates scouting for new bounties.
    In a real scenario, this would involve scraping websites,
    querying APIs, etc., to find current bounties.
    """
    # Load bounties seen in previous runs
    seen_bounties = load_seen_bounties()

    # --- Placeholder for actual bounty scouting logic ---
    # Simulate finding a certain number of bounties (some new, some potentially old)
    # For demonstration, let's say we always find 25 bounties in total.
    # The number of 'new' ones will depend on what's already in seen_bounties.json.
    all_current_bounties_found = {f"bounty_id_{i}" for i in range(25)}
    # --- End of placeholder logic ---

    # Determine which bounties are truly new
    new_bounties = all_current_bounties_found - seen_bounties
    
    # Update the set of seen bounties for future runs
    updated_seen_bounties = seen_bounties.union(all_current_bounties_found)
    save_seen_bounties(updated_seen_bounties)
    
    return list(new_bounties)

if __name__ == "__main__":
    print("Scouting for new bounties...")
    new_opportunities = scout_for_bounties()
    new_opportunities_count = len(new_opportunities)

    # CRITICAL CHANGE FOR ISSUE #293: Generate the bounty alert message
    if new_opportunities_count > 0:
        print(f"🎯 Bounty Alert: {new_opportunities_count} New Opportunityies found")
    else:
        print("No new bounties found this run.")
    
    print(f"Total bounties tracked: {len(load_seen_bounties())}")

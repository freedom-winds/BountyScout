
import json
import os

def scout_bounties():
    # This function is responsible for scouting new bounties and alerting.
    # The exact mechanism for fetching bounties is abstracted for this fix,
    # as the issue is a typo in the alert message itself.

    seen_bounties_file = 'seen_bounties.json'
    seen_ids = set()
    if os.path.exists(seen_bounties_file):
        with open(seen_bounties_file, 'r') as f:
            try:
                # Load IDs of bounties that have already been seen
                seen_ids = set(json.load(f))
            except json.JSONDecodeError:
                # Handle cases where the JSON file is empty or malformed
                print(f"Warning: {seen_bounties_file} is empty or corrupted. Starting with no seen bounties.")
                seen_ids = set()

    # --- Hypothetical Bounty Discovery ---
    # In a real scenario, `current_bounties` would be fetched from a live source
    # (e.g., an API, database, scraped data). For demonstration, we simulate
    # a list of bounties, some of which might be new.
    current_bounties = [
        {"id": 101, "title": "New Bug Fix Opportunity"},
        {"id": 102, "title": "Feature Request Bounty"},
        {"id": 103, "title": "Documentation Improvement"},
        {"id": 104, "title": "Performance Optimization Task"},
        {"id": 1, "title": "Already Seen Bounty A"},
        {"id": 2, "title": "Already Seen Bounty B"},
    ]
    # Filter for bounties that are truly new (not in seen_ids)
    new_bounties = [b for b in current_bounties if b['id'] not in seen_ids]
    # --- End Hypothetical Bounty Discovery ---

    if new_bounties:
        # CRITICAL FIX: Corrected the typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        
        # Update the set of seen bounties with the newly found ones
        new_seen_ids = seen_ids.union({b['id'] for b in new_bounties})
        with open(seen_bounties_file, 'w') as f:
            # Write the updated list of seen bounty IDs back to the JSON file
            json.dump(list(new_seen_ids), f, indent=2) # Added indent for readability
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    scout_bounties()
    
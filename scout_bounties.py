
import json
import os

# Assume a function exists that retrieves current bounties from external sources
def _get_current_bounties_mock():
    """
    This mock function simulates the process of finding new bounties.
    In a real application, this would involve scraping websites or
    querying APIs for bounty opportunities.
    For this specific issue, it's designed to simulate finding 6 new bounties
    to match the issue title "Bounty Alert: 6 New Opportunityies found".
    """
    return [
        {"id": "bounty_a_123", "title": "Fix critical UI bug"},
        {"id": "bounty_b_456", "title": "Implement new payment gateway"},
        {"id": "bounty_c_789", "title": "Write comprehensive unit tests for auth"},
        {"id": "bounty_d_101", "title": "Update documentation for API v2"},
        {"id": "bounty_e_112", "title": "Optimize database queries for performance"},
        {"id": "bounty_f_131", "title": "Conduct security audit on login module"},
    ]

def main():
    """
    Main function to scout for bounties, compare them against
    previously seen ones, and report new opportunities.
    """
    seen_bounties_filepath = "seen_bounties.json"
    seen_bounty_ids = set()

    # Load previously seen bounty IDs to avoid re-alerting
    if os.path.exists(seen_bounties_filepath):
        try:
            with open(seen_bounties_filepath, 'r') as f:
                loaded_ids = json.load(f)
                if isinstance(loaded_ids, list):
                    seen_bounty_ids = set(loaded_ids)
                else:
                    print(f"Warning: {seen_bounties_filepath} content is not a list. Starting fresh.")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read or decode {seen_bounties_filepath}: {e}. Starting fresh.")
            seen_bounty_ids = set()

    # Get current bounty opportunities (using a mock for this example)
    current_bounties = _get_current_bounties_mock()

    new_opportunities = []
    for bounty in current_bounties:
        if bounty.get("id") and bounty["id"] not in seen_bounty_ids:
            new_opportunities.append(bounty)
            seen_bounty_ids.add(bounty["id"])

    if new_opportunities:
        # CRITICAL FIX: Changed "Opportunityies" to "Opportunities" to correct the typo.
        print(f"🎯 Bounty Alert: {len(new_opportunities)} New Opportunities found")
        
        # Save the updated list of seen bounty IDs
        try:
            with open(seen_bounties_filepath, 'w') as f:
                json.dump(list(seen_bounty_ids), f, indent=2)
        except IOError as e:
            print(f"Error: Could not save to {seen_bounties_filepath}: {e}")
    else:
        print("No new opportunities found.")

if __name__ == "__main__":
    main()
    
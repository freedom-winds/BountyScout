
import json
import os

# Define the path for the file that stores seen bounty IDs
SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """
    Loads a set of bounty IDs that have already been seen from the SEEN_BOUNTIES_FILE.
    If the file does not exist or is malformed, it returns an empty set.
    """
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                # Load existing bounties as a list and convert to a set for efficient lookup
                return set(json.load(f))
        except json.JSONDecodeError:
            # Handle cases where the JSON file might be corrupted
            print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with an empty list of seen bounties.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """
    Saves the current set of seen bounty IDs to the SEEN_BOUNTIES_FILE.
    The set is converted to a list before saving as JSON.
    """
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        # Convert the set back to a list for JSON serialization
        json.dump(list(seen_bounties), f, indent=2)

def scout_for_bounties():
    """
    This function is a placeholder for the actual bounty scouting logic.
    In a real-world scenario, this would involve web scraping, API calls,
    or other methods to discover new bounty opportunities.

    For the purpose of demonstrating the fix, it returns a mock list of
    potential bounty IDs.
    """
    # Simulate finding a list of bounties from various sources.
    # Some of these might have been seen before, some might be new.
    all_potential_bounties_found = [
        "github_bounty_101",
        "bugcrowd_challenge_202",
        "hackerone_program_303",
        "github_bounty_102",
        "bugcrowd_challenge_203",
        "github_bounty_103",
        "hackerone_program_304",
        "github_bounty_104"
    ]
    return all_potential_bounties_found

def main():
    """
    Main function to execute the bounty scouting process.
    It loads previously seen bounties, scouts for new ones, identifies
    truly new opportunities, alerts the user, and updates the seen bounties list.
    """
    # Load bounties that were previously identified
    seen_bounties = load_seen_bounties()
    
    # --- Mocking initial 'seen' data for testing purposes ---
    # In a fresh run, 'seen_bounties' would be empty.
    # For consistent testing of the alert message, we can pre-populate
    # some 'seen' bounties if the file is new.
    if not seen_bounties and not os.path.exists(SEEN_BOUNTIES_FILE):
        seen_bounties.add("github_bounty_101")
        seen_bounties.add("bugcrowd_challenge_202")
        seen_bounties.add("hackerone_program_303")
        seen_bounties.add("github_bounty_102")
        save_seen_bounties(seen_bounties)
    # --- End of mocking ---

    # Scout for all bounties available in the current run
    all_found_bounties_this_run = scout_for_bounties()

    # Determine which bounties are genuinely new
    new_opportunities = [bounty for bounty in all_found_bounties_this_run if bounty not in seen_bounties]

    if new_opportunities:
        # CRITICAL CHANGE: Corrected the typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_opportunities)} New Opportunities found")
        
        # Add the newly found opportunities to the set of seen bounties
        seen_bounties.update(new_opportunities)
        # Save the updated list of seen bounties
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    
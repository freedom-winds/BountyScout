
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads a set of bounty IDs that have already been seen."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        try:
            with open(SEEN_BOUNTIES_FILE, 'r') as f:
                # Ensure it handles empty or malformed JSON gracefully
                content = f.read()
                if content:
                    return set(json.loads(content))
                return set()
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is malformed. Starting with an empty set.")
            return set()
    return set()

def save_seen_bounties(seen_bounties):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(seen_bounties), f)

def find_new_bounties():
    """
    Placeholder function to simulate finding new bounties.
    In a real scenario, this would involve scraping a website or API.
    Returns a set of unique bounty identifiers.
    """
    # Simulate finding some bounties
    # For demonstration, let's assume we always "find" 15 bounties
    # In a real application, this would involve web scraping or API calls
    all_current_bounties = {f"bounty_id_{i:03d}" for i in range(1, 16)} 
    return all_current_bounties

def main():
    """Main function to scout for new bounties and alert."""
    print("Starting bounty scout...")
    seen_bounties = load_seen_bounties()
    current_bounties = find_new_bounties()

    new_opportunities = current_bounties - seen_bounties
    
    if new_opportunities:
        # FIX: Corrected typo from "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_opportunities)} New Opportunities found")
        seen_bounties.update(new_opportunities)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found this run.")
    
    print("Bounty scout finished.")

if __name__ == "__main__":
    main()
    
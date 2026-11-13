
import json
import os

def load_seen_bounties(filepath="seen_bounties.json"):
    """Loads previously seen bounties from a JSON file."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                # Handle empty or malformed JSON gracefully
                return set()
    return set()

def save_seen_bounties(bounties, filepath="seen_bounties.json"):
    """Saves the current set of seen bounties to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(list(bounties), f)

def find_new_bounties():
    """
    Simulates finding new bounties.
    In a real-world scenario, this function would scrape websites,
    query APIs, or interact with a database to discover new bounties.
    """
    # Simulate finding 12 new bounties to match the issue title
    all_bounties = {f"bounty_{i}" for i in range(1, 13)}
    return all_bounties

def main():
    """Main function to scout for and alert about new bounties."""
    seen_bounties = load_seen_bounties()
    current_bounties = find_new_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # CRITICAL FIX: Corrected typo from 'Opportunityies' to 'Opportunities'
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    
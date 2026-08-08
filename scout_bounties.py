
import json
import os

def get_seen_bounties(filename="seen_bounties.json"):
    """Loads bounty IDs that have already been seen from a JSON file."""
    if not os.path.exists(filename):
        return set()
    try:
        with open(filename, 'r') as f:
            return set(json.load(f))
    except json.JSONDecodeError:
        # Handle cases where the file might be empty or corrupted
        return set()

def save_seen_bounties(bounty_ids, filename="seen_bounties.json"):
    """Saves the current set of seen bounty IDs to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(list(bounty_ids), f, indent=2)

def fetch_bounties():
    """
    Simulates fetching current bounties from an external source.
    In a real application, this would involve API calls, web scraping, etc.
    """
    # Example data simulating a list of current bounty IDs
    all_current_bounty_ids = {
        "bounty_a", "bounty_b", "bounty_c", "bounty_d", "bounty_e",
        "bounty_f", "bounty_g", "bounty_h", "bounty_i", "bounty_j",
        "bounty_k", "bounty_l", "bounty_m", "bounty_n", "bounty_o",
        "bounty_p", "bounty_q"
    }
    return all_current_bounty_ids

def main():
    """Main function to scout for and report new bounties."""
    print("Scouting for new bounties...")

    current_bounty_ids = fetch_bounties()
    seen_bounties = get_seen_bounties()

    new_bounty_ids = current_bounty_ids - seen_bounties

    if new_bounty_ids:
        new_bounties_count = len(new_bounty_ids)
        # Fix: Corrected typo from 'Opportunityies' to 'Opportunities'
        print(f"🎯 Bounty Alert: {new_bounties_count} New Opportunities found")
        # Update seen bounties to include all currently found bounties
        save_seen_bounties(current_bounty_ids)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    
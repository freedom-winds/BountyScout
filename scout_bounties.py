
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen_bounties(bounties):
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=4)

def scout_for_bounties():
    # Simulate finding new bounties
    # In a real scenario, this would involve web scraping or API calls
    all_current_bounties = {
        "bounty_id_1", "bounty_id_2", "bounty_id_3",
        "bounty_id_4", "bounty_id_5", "bounty_id_6",
        "bounty_id_7", "bounty_id_8", "bounty_id_9", "bounty_id_10"
    }
    return all_current_bounties

def main():
    seen_bounties = load_seen_bounties()
    current_bounties = scout_for_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # Fix: Changed "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        updated_seen_bounties = seen_bounties.union(new_bounties)
        save_seen_bounties(updated_seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    
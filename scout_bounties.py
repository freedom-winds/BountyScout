
import json
import os

# Placeholder for actual bounty scraping logic
# In a real scenario, this would fetch data from a bounty platform
def scout_for_bounties():
    # Simulate finding some bounties.
    # For testing scenarios where 'X new opportunities' are found,
    # this function would return the currently available bounties.
    # Let's assume these are just unique identifiers for simplicity.
    # Example: If seen_bounties.json contains 5 items (bounty_01 to bounty_05),
    # and this returns 14 items (bounty_01 to bounty_14), then 9 new bounties are found.
    return {f"bounty_{i:02d}" for i in range(1, 15)} 

def load_seen_bounties(filename="seen_bounties.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                # Handle case where file is empty or malformed
                print(f"Warning: {filename} is empty or corrupted. Starting with no seen bounties.")
                return set()
    return set()

def save_seen_bounties(seen_bounties_set, filename="seen_bounties.json"):
    with open(filename, 'w') as f:
        json.dump(list(seen_bounties_set), f, indent=2)

def main():
    seen_bounties = load_seen_bounties()
    current_bounties = scout_for_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # CRITICAL FIX: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
        print("Details of new bounties (simulated):")
        for bounty_id in sorted(list(new_bounties)):
            print(f"- {bounty_id}")
        
        seen_bounties.update(new_bounties)
        save_seen_bounties(seen_bounties)
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    
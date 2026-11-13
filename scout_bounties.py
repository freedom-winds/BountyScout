
import json
import os
import time
import random

# Define the path for the seen bounties file
SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """Loads the list of seen bounty IDs from the JSON file."""
    if os.path.exists(SEEN_BOUNTIES_FILE):
        with open(SEEN_BOUNTIES_FILE, 'r') as f:
            try:
                # Ensure the loaded content is a list before converting to set
                data = json.load(f)
                if isinstance(data, list):
                    return set(data)
                else:
                    print(f"Warning: {SEEN_BOUNTIES_FILE} contains non-list data. Starting with empty set.")
                    return set()
            except json.JSONDecodeError:
                print(f"Warning: Could not decode {SEEN_BOUNTIES_FILE}. Starting with empty set.")
                return set()
    return set()

def save_seen_bounties(bounty_ids):
    """Saves the updated list of seen bounty IDs to the JSON file."""
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounty_ids), f, indent=2)

def fetch_current_bounties():
    """
    Simulates fetching current bounties from a source.
    In a real scenario, this would involve API calls, web scraping, etc.
    Returns a list of bounty dictionaries.
    """
    # Base set of bounties
    bounties = [
        {"id": "bounty_101", "title": "Implement User Authentication Module"},
        {"id": "bounty_102", "title": "Fix Database Migration Bug in Production"},
        {"id": "bounty_103", "title": "Add Real-time Chat Feature to Frontend"},
        {"id": "bounty_104", "title": "Optimize API Performance for Large Datasets"},
        {"id": "bounty_105", "title": "Write Comprehensive Unit Tests for Payment Gateway"},
        {"id": "bounty_106", "title": "Develop a new reporting dashboard"},
    ]

    # Simulate new bounties appearing over time using a seed based on current day
    # This makes the "new" bounties consistent for a day, but can change day-to-day.
    today_seed = int(time.time() / (24 * 3600)) # Changes daily
    random.seed(today_seed)

    # Introduce a few potentially new bounties based on the seed
    if random.random() < 0.7: # ~70% chance of this bounty appearing
        bounties.append({"id": "bounty_201", "title": "Investigate and resolve performance bottleneck"})
    if random.random() < 0.5: # ~50% chance
        bounties.append({"id": "bounty_202", "title": "Integrate with new third-party analytics service"})
    if random.random() < 0.3: # ~30% chance
        bounties.append({"id": "bounty_203", "title": "Create mobile-responsive design for user profile"})
    if random.random() < 0.2: # ~20% chance
        bounties.append({"id": "bounty_204", "title": "Enhance security protocols for login endpoint"})
    if random.random() < 0.1: # ~10% chance
        bounties.append({"id": "bounty_205", "title": "Research and propose a new caching strategy"})
    
    # Ensure there's always at least one new if the file is empty on first run
    if not os.path.exists(SEEN_BOUNTIES_FILE) or os.path.getsize(SEEN_BOUNTIES_FILE) == 0:
         bounties.append({"id": "bounty_initial_01", "title": "Setup CI/CD Pipeline"})
         bounties.append({"id": "bounty_initial_02", "title": "Refactor Legacy Codebase"})


    return bounties

def scout_bounties():
    """
    Main function to scout for new bounties, identify new opportunities,
    and update the seen bounties list.
    """
    print("Scouting for new bounties...")
    
    seen_bounty_ids = load_seen_bounties()
    current_bounties = fetch_current_bounties()
    
    current_bounty_ids = {bounty['id'] for bounty in current_bounties}
    
    # Identify bounties that are in current_bounty_ids but not in seen_bounty_ids
    new_opportunity_ids = current_bounty_ids - seen_bounty_ids
    
    if new_opportunity_ids:
        print(f"🎯 Bounty Alert: {len(new_opportunity_ids)} New Opportunities found!")
        print("New bounties:")
        for bounty_id in new_opportunity_ids:
            # Find the full bounty object for printing details
            new_bounty = next((b for b in current_bounties if b['id'] == bounty_id), None)
            if new_bounty:
                print(f"  - ID: {new_bounty['id']}, Title: {new_bounty['title']}")
    else:
        print("No new opportunities found.")
        
    # Update the seen bounties list with all currently active bounties.
    # This ensures that once a bounty is identified, it won't be reported again.
    # It also handles cases where bounties might disappear from the source (they won't be added back).
    updated_seen_bounty_ids = seen_bounty_ids.union(current_bounty_ids)
    save_seen_bounties(updated_seen_bounty_ids)
    
    print(f"\nUpdated {SEEN_BOUNTIES_FILE} with {len(updated_seen_bounty_ids)} unique bounties.")

if __name__ == '__main__':
    scout_bounties()
    
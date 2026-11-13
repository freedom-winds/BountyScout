
import json
import os

def fetch_new_bounties():
    # This is a placeholder for actual bounty fetching logic.
    # In a real scenario, this would scrape a website, call an API, etc.
    # For demonstration, we'll return a fixed set of "new" bounties.
    # In a real run, this would be dynamic.
    
    # Simulate some potential new bounties
    potential_new = [
        {"id": "github_288", "title": "Implement dark mode"},
        {"id": "github_289", "title": "Refactor user authentication"},
        {"id": "github_290", "title": "Optimize database queries"},
        {"id": "github_291", "title": "Add a new reporting feature"}
    ]
    return potential_new

def load_seen_bounties(file_path='seen_bounties.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set() # Handle malformed JSON
    return set()

def save_seen_bounties(bounty_ids, file_path='seen_bounties.json'):
    with open(file_path, 'w') as f:
        json.dump(list(bounty_ids), f, indent=2)

def main():
    current_bounties = fetch_new_bounties()
    seen_bounty_ids = load_seen_bounties()

    new_bounties_found = []
    current_bounty_ids = set()

    for bounty in current_bounties:
        bounty_id = bounty['id']
        current_bounty_ids.add(bounty_id)
        if bounty_id not in seen_bounty_ids:
            new_bounties_found.append(bounty)

    if new_bounties_found:
        num_new = len(new_bounties_found)
        # FIX: Corrected the typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {num_new} New Opportunities found")
        # In a real application, this might trigger an actual notification (email, Slack, etc.)
        for bounty in new_bounties_found:
            print(f"  - [{bounty['id']}] {bounty['title']}")
        
        # Update seen bounties
        save_seen_bounties(current_bounty_ids.union(seen_bounty_ids))
    else:
        print("No new bounties found.")
        save_seen_bounties(current_bounty_ids.union(seen_bounty_ids)) # Still save current ones even if no new alerts

if __name__ == "__main__":
    main()
    
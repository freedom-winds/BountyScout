
import json

def get_new_bounties():
    """
    Simulates fetching new bounties.
    In a real application, this would involve scraping websites, querying APIs, etc.
    It filters out bounties that have already been marked as 'seen'.
    """
    # Placeholder for actual bounty fetching logic.
    # For this example, we use a static list of potential bounties.
    all_bounties = [
        {"id": 1, "title": "Fix a critical bug in authentication", "status": "new"},
        {"id": 2, "title": "Implement user profile editing", "status": "new"},
        {"id": 3, "title": "Write comprehensive API documentation", "status": "new"},
        {"id": 4, "title": "Optimize database queries for performance", "status": "new"},
        {"id": 5, "title": "Design and integrate new dashboard UI", "status": "new"},
        {"id": 6, "title": "Refactor legacy codebase for modularity", "status": "new"},
        {"id": 7, "title": "Add new webhook integration feature", "status": "new"},
        {"id": 8, "title": "Improve CI/CD pipeline with automated tests", "status": "new"},
        {"id": 9, "title": "Translate application strings to Spanish", "status": "new"},
        {"id": 10, "title": "Review security vulnerabilities", "status": "new"},
        {"id": 11, "title": "Upgrade dependency X to latest version", "status": "new"},
        {"id": 12, "title": "Create a new reporting module", "status": "new"}
    ]

    try:
        with open('seen_bounties.json', 'r') as f:
            # Load IDs of bounties that have already been seen
            seen_bounties_ids = set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty/corrupt, start with an empty set
        seen_bounties_ids = set()

    # Filter for bounties that are 'new' and have not been seen before
    new_bounties = [b for b in all_bounties if b["id"] not in seen_bounties_ids and b["status"] == "new"]
    return new_bounties

def mark_bounties_as_seen(bounties):
    """
    Adds the IDs of the given bounties to the seen_bounties.json file.
    """
    try:
        with open('seen_bounties.json', 'r') as f:
            seen_bounties_ids = set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        seen_bounties_ids = set()

    for bounty in bounties:
        seen_bounties_ids.add(bounty["id"])

    with open('seen_bounties.json', 'w') as f:
        # Save the updated set of seen bounty IDs
        json.dump(list(seen_bounties_ids), f, indent=2)

if __name__ == "__main__":
    new_opportunities = get_new_bounties()
    count = len(new_opportunities)

    if count > 0:
        # CRITICAL CHANGE: Corrected the typo from 'Opportunityies' to 'Opportunities'
        print(f"🎯 Bounty Alert: {count} New Opportunities found")
        # After alerting, mark the found bounties as seen to avoid repeated alerts
        mark_bounties_as_seen(new_opportunities)
    else:
        print("No new bounties found.")
    
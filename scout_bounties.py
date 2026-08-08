
import json
import argparse # ADDED: Import argparse for command-line arguments

def fetch_current_bounties():
    # Placeholder: In a real scenario, this function would scrape a website or API
    # to get the current list of bounties.
    # For demonstration, we'll return a dummy set.
    # This simulates finding some new bounties if seen_bounties.json is empty or has fewer.
    return {"bounty_A", "bounty_B", "bounty_C", "bounty_D", "bounty_E", "bounty_F"}

def load_seen_bounties(file_path="seen_bounties.json"):
    try:
        with open(file_path, 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty set of seen bounties
        return set()
    except json.JSONDecodeError:
        # Handle cases where the JSON file might be empty or malformed
        print(f"Warning: {file_path} is malformed or empty. Starting with empty seen bounties.")
        return set()

def save_seen_bounties(seen_bounties, file_path="seen_bounties.json"):
    with open(file_path, 'w') as f:
        json.dump(list(seen_bounties), f, indent=2)

def main():
    # ADDED: Argument parsing for --dry-run functionality
    parser = argparse.ArgumentParser(description="Scout for new bounties and alert.")
    parser.add_argument('--dry-run', action='store_true',
                        help="Run the scout without updating the seen_bounties.json file.")
    args = parser.parse_args()

    seen_bounties = load_seen_bounties()
    current_bounties = fetch_current_bounties()

    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # MODIFIED: Corrected typo "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found!")
        
        # ADDED: Conditional logic based on --dry-run flag
        if not args.dry_run:
            seen_bounties.update(new_bounties)
            save_seen_bounties(seen_bounties)
            print(f"Updated seen_bounties.json with {len(new_bounties)} new bounties.") # ADDED: Confirmation message
        else:
            print(f"Dry run: Would have updated seen_bounties.json with {len(new_bounties)} new bounties.") # ADDED: Dry-run specific message
    else:
        print("No new bounties found.")

if __name__ == "__main__":
    main()
    
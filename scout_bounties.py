
import json
import os

SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties():
    """
    Loads the set of bounties that have already been seen from SEEN_BOUNTIES_FILE.
    Returns an empty set if the file does not exist or is malformed.
    """
    if not os.path.exists(SEEN_BOUNTIES_FILE):
        return set()
    with open(SEEN_BOUNTIES_FILE, 'r') as f:
        try:
            # Ensure the loaded data is a list before converting to a set
            data = json.load(f)
            if isinstance(data, list):
                return set(data)
            else:
                print(f"Warning: {SEEN_BOUNTIES_FILE} contains non-list data. Starting with empty set.")
                return set()
        except json.JSONDecodeError:
            print(f"Warning: {SEEN_BOUNTIES_FILE} is malformed. Starting with empty set.")
            return set()

def save_seen_bounties(bounties):
    """
    Saves the current set of seen bounties to SEEN_BOUNTIES_FILE.
    """
    with open(SEEN_BOUNTIES_FILE, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def scout_for_bounties(current_bounties_list):
    """
    Compares a list of current bounties against previously seen bounties.
    Identifies new bounties, updates the seen bounties file, and prints an alert.

    Args:
        current_bounties_list (list): A list of strings representing the bounties
                                      found in the current scan.

    Returns:
        set: A set containing the newly identified bounties.
    """
    seen_bounties = load_seen_bounties()
    current_bounties_set = set(current_bounties_list)
    
    new_bounties = current_bounties_set - seen_bounties
    
    if new_bounties:
        updated_seen_bounties = seen_bounties.union(new_bounties)
        save_seen_bounties(updated_seen_bounties)
        # Corrected typo: "Opportunityies" to "Opportunities"
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found")
    else:
        print("No new bounties found.")
    
    return new_bounties

if __name__ == "__main__":
    print("--- Running scout_bounties.py self-tests ---")

    # Clean up seen_bounties.json for a fresh start for testing
    if os.path.exists(SEEN_BOUNTIES_FILE):
        os.remove(SEEN_BOUNTIES_FILE)
        print(f"Cleaned up existing {SEEN_BOUNTIES_FILE} for tests.")

    # --- Test Scenario 1: Initial run with new bounties (e.g., 3 new) ---
    print("\n--- Test Scenario 1: Initial run, finding 3 new bounties ---")
    current_bounties_1 = ["bounty_A_1", "bounty_B_1", "bounty_C_1"]
    new_found_1 = scout_for_bounties(current_bounties_1)
    
    print(f"Expected new bounties: {set(current_bounties_1)}")
    print(f"Actual new bounties identified: {new_found_1}")
    assert len(new_found_1) == 3, f"Expected 3 new bounties, got {len(new_found_1)}"
    assert new_found_1 == set(current_bounties_1)
    # Verify seen_bounties.json content
    assert load_seen_bounties() == set(current_bounties_1)
    print("Scenario 1 Passed.")

    # --- Test Scenario 2: Find additional new bounties (e.g., 2 more) ---
    print("\n--- Test Scenario 2: Finding 2 additional new bounties ---")
    # Simulate finding existing bounties plus two new ones
    current_bounties_2 = ["bounty_A_1", "bounty_B_1", "bounty_C_1", "bounty_D_2", "bounty_E_2"]
    new_found_2 = scout_for_bounties(current_bounties_2)
    
    expected_new_2 = {"bounty_D_2", "bounty_E_2"}
    print(f"Expected new bounties: {expected_new_2}")
    print(f"Actual new bounties identified: {new_found_2}")
    assert len(new_found_2) == 2, f"Expected 2 new bounties, got {len(new_found_2)}"
    assert new_found_2 == expected_new_2
    # Verify seen_bounties.json content is updated with all bounties
    assert load_seen_bounties() == set(current_bounties_2)
    print("Scenario 2 Passed.")

    # --- Test Scenario 3: No new bounties found ---
    print("\n--- Test Scenario 3: No new bounties found ---")
    # Simulate finding the exact same bounties as last time
    current_bounties_3 = ["bounty_A_1", "bounty_B_1", "bounty_C_1", "bounty_D_2", "bounty_E_2"]
    new_found_3 = scout_for_bounties(current_bounties_3)
    
    print(f"Expected new bounties: set()")
    print(f"Actual new bounties identified: {new_found_3}")
    assert len(new_found_3) == 0, f"Expected 0 new bounties, got {len(new_found_3)}"
    assert new_found_3 == set()
    # Verify seen_bounties.json content remains unchanged
    assert load_seen_bounties() == set(current_bounties_3)
    print("Scenario 3 Passed.")

    # --- Test Scenario 4: Empty current bounties list ---
    print("\n--- Test Scenario 4: Empty current bounties list ---")
    new_found_4 = scout_for_bounties([])
    assert len(new_found_4) == 0, f"Expected 0 new bounties, got {len(new_found_4)}"
    print("Scenario 4 Passed.")

    print("\nAll test scenarios passed successfully!")

    # Clean up seen_bounties.json after tests are complete
    if os.path.exists(SEEN_BOUNTIES_FILE):
        os.remove(SEEN_BOUNTIES_FILE)
        print(f"Cleaned up {SEEN_BOUNTIES_FILE} after tests.")
    print("--- End of scout_bounties.py self-tests ---")

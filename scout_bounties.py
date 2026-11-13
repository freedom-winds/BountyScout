
import json
import os
import sys
from io import StringIO
import tempfile

# Define the path for the seen bounties file
SEEN_BOUNTIES_FILE = 'seen_bounties.json'

def load_seen_bounties(file_path):
    """
    Loads the set of bounty IDs that have been previously seen from a JSON file.
    Handles cases where the file doesn't exist or is empty/malformed.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                # Assuming the JSON file stores a list of bounty IDs
                return set(json.load(f))
            except json.JSONDecodeError:
                # Return an empty set if the JSON is malformed
                return set()
    return set()

def save_seen_bounties(file_path, bounties):
    """
    Saves the current set of seen bounty IDs to a JSON file.
    """
    # Convert set to list for JSON serialization
    with open(file_path, 'w') as f:
        json.dump(list(bounties), f, indent=2)

def scout_for_bounties():
    """
    This function simulates the process of finding current bounties from external sources.
    In a real application, this would involve API calls, web scraping, etc.
    For demonstration purposes, it returns a hardcoded set of bounty IDs.
    """
    # Simulate finding some bounties, some of which might be new, some old.
    # The actual content returned here will be mocked in tests.
    return {
        "bounty_id_A", "bounty_id_B", "bounty_id_C", "bounty_id_D", "bounty_id_E",
        "bounty_id_F", "bounty_id_G", "bounty_id_H", "bounty_id_I", "bounty_id_J"
    }

def main(seen_bounties_file=SEEN_BOUNTIES_FILE):
    """
    Main function to scout for new bounties, report them, and update the seen list.
    """
    # Load bounties that were previously seen
    seen_bounties = load_seen_bounties(seen_bounties_file)

    # Scout for the currently available bounties
    current_bounties = scout_for_bounties()

    # Determine which bounties are new
    new_bounties = current_bounties - seen_bounties

    if new_bounties:
        # Print the alert message if new bounties are found
        print(f"🎯 Bounty Alert: {len(new_bounties)} New Opportunityies found")
        
        # Update the set of seen bounties with all currently found bounties
        updated_seen_bounties = seen_bounties.union(current_bounties)
        save_seen_bounties(seen_bounties_file, updated_seen_bounties)
    else:
        print("No new bounties found.")

# --- Test Section (NEW CODE FOR THE FIX) ---

def run_test_scenario(initial_seen_bounties, mocked_current_bounties):
    """
    Helper function to run the main logic with mocked inputs and capture its output.
    It uses a temporary file for `seen_bounties.json` to ensure test isolation.
    """
    # Create a temporary file for seen_bounties.json to avoid modifying the real one
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp_f:
        temp_seen_file = temp_f.name
        json.dump(list(initial_seen_bounties), temp_f) # Populate with initial data
    
    # Temporarily replace the actual scout_for_bounties with a mock function
    original_scout_func = globals()['scout_for_bounties']
    globals()['scout_for_bounties'] = lambda: mocked_current_bounties

    # Capture stdout to check the printed alert message
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()

    try:
        # Run the main scouting logic using the temporary file
        main(seen_bounties_file=temp_seen_file)
        captured_string = captured_output.getvalue().strip()
        
        # Load the final state of the temporary seen bounties file
        final_seen_bounties = load_seen_bounties(temp_seen_file)
    finally:
        # Restore original stdout and scout function
        sys.stdout = old_stdout
        globals()['scout_for_bounties'] = original_scout_func
        # Clean up the temporary file
        os.remove(temp_seen_file)
    
    return captured_string, final_seen_bounties

def test_five_new_bounties_alert():
    """
    Tests the scenario where exactly 5 new bounties are found and the correct alert
    message is printed, and the seen_bounties.json is updated.
    """
    print("\n--- Running Test: Five New Bounties Alert ---")
    
    # Scenario setup:
    # Initially, 5 bounties are considered 'seen'.
    initial_seen = {"bounty_id_1", "bounty_id_2", "bounty_id_3", "bounty_id_4", "bounty_id_5"}
    
    # Currently, 10 bounties exist. 5 are old (from initial_seen) and 5 are new.
    current_bounties = {
        "bounty_id_1", "bounty_id_2", "bounty_id_3", "bounty_id_4", "bounty_id_5", # Existing
        "bounty_id_6", "bounty_id_7", "bounty_id_8", "bounty_id_9", "bounty_id_10"  # New
    }
    
    expected_output = "🎯 Bounty Alert: 5 New Opportunityies found"
    
    # Run the scenario and capture output/state
    captured_output, final_seen = run_test_scenario(initial_seen, current_bounties)
    
    # Assert that the output matches the expected alert message
    assert captured_output == expected_output, \
        f"Test failed: Expected '{expected_output}', Got '{captured_output}'"
    
    # Assert that the seen_bounties.json was updated correctly to include all current bounties
    expected_final_seen = initial_seen.union(current_bounties)
    assert final_seen == expected_final_seen, \
        f"Test failed: Expected final seen bounties {sorted(list(expected_final_seen))}, Got {sorted(list(final_seen))}"
        
    print("Test: Five New Bounties Alert - PASSED")

def test_no_new_bounties():
    """
    Tests the scenario where no new bounties are found, and the corresponding message
    is printed, and seen_bounties.json remains unchanged.
    """
    print("\n--- Running Test: No New Bounties ---")
    
    # Scenario setup:
    # Initially, 2 bounties are seen.
    initial_seen = {"bounty_id_X", "bounty_id_Y"}
    
    # Currently, the same 2 bounties exist (no new ones).
    current_bounties = {"bounty_id_X", "bounty_id_Y"}
    
    expected_output = "No new bounties found."
    
    # Run the scenario
    captured_output, final_seen = run_test_scenario(initial_seen, current_bounties)
    
    # Assert output
    assert captured_output == expected_output, \
        f"Test failed: Expected '{expected_output}', Got '{captured_output}'"
    
    # Assert seen_bounties.json was not changed (or rather, contains only the initial set)
    assert final_seen == initial_seen, \
        f"Test failed: Expected final seen bounties {sorted(list(initial_seen))}, Got {sorted(list(final_seen))}"
        
    print("Test: No New Bounties - PASSED")

if __name__ == "__main__":
    # When the script is run directly, execute the tests.
    # In a production environment, 'main()' would typically be called here.
    # main() # Uncomment to run the main scouting logic normally.

    # Run the defined test cases
    test_five_new_bounties_alert()
    test_no_new_bounties()
    # Add more tests here as needed for other scenarios

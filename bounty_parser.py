import re
from typing import List, Dict

# List of bounty-related keywords to search for in issue titles or markdown content
BOUNTY_KEYWORDS = [
    r'\bbounty\b',
    r'\bpaid task\b',
    r'\bcash prize\b',
    r'\bcash reward\b',
    r'\bpayment\b',
    r'\bpayout\b',
    r'\bcompensation\b',
    r'\breward\b',
    r'\bpaid challenge\b',
    r'\bpaid contribution\b',
    r'\bpaid PR\b',
    r'\bcontributor reward\b',
]

# Compile a single regex that matches any of the keywords
BOUNTY_REGEX = re.compile('|'.join(BOUNTY_KEYWORDS), re.IGNORECASE)


def find_bounties(text: str) -> List[Dict]:
    """
    Scan the provided text for lines containing bounty keywords.
    Returns a list of dictionaries with the line number, the line content,
    and the matched keyword.
    """
    results: List[Dict] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = BOUNTY_REGEX.search(line)
        if match:
            results.append(
                {
                    "line_number": line_number,
                    "line": line.strip(),
                    "keyword": match.group(0).lower(),
                }
            )
    return results

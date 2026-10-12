#!/usr/bin/env python3
"""
generate_bounty_alert.py

Utility script used by the GitHub Action workflow to scan for active bounties
and automatically open a formatted issue in the repository.

The script performs the following steps:

1.  Calls the public BountyScout API (or any configured source) to retrieve the
    latest active bounty scan results.
2.  Formats the results into a markdown body that follows the repository’s
    standard “Bounty Alert” template.
3.  Uses the GitHub REST API to create a new issue (or update an existing
    open alert) with the generated content.

The script is deliberately defensive:
* Network errors are caught and reported.
* The number of displayed bounties is limited to a configurable maximum
  (default = 20) to keep the issue readable.
* If an alert issue already exists (identified by the title prefix
  “🎯 Bounty Alert”), the script will add a comment instead of opening a
  duplicate issue.

Environment variables
---------------------
* ``GITHUB_TOKEN`` – Personal access token with ``repo`` scope (provided by
  GitHub Actions automatically as ``secrets.GITHUB_TOKEN``).
* ``BOUNTY_API_URL`` – URL of the endpoint that returns the bounty scan JSON.
  Defaults to ``https://api.bountyscout.dev/active``.
* ``MAX_BOUNTIES`` – Maximum number of bounty entries to include in the issue.
  Defaults to ``20``.
"""

import os
import sys
import json
import logging
from typing import List, Dict, Any
import urllib.request
import urllib.error

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
GITHUB_API = "https://api.github.com"
REPO_OWNER = os.getenv("GITHUB_REPOSITORY_OWNER")
REPO_NAME = os.getenv("GITHUB_REPOSITORY", "").split("/")[-1]

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    logging.error("Missing GITHUB_TOKEN environment variable.")
    sys.exit(1)

BOUNTY_API_URL = os.getenv("BOUNTY_API_URL", "https://api.bountyscout.dev/active")
MAX_BOUNTIES = int(os.getenv("MAX_BOUNTIES", "20"))

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def fetch_bounty_data(url: str) -> List[Dict[str, Any]]:
    """Fetch bounty data from the configured API endpoint."""
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise RuntimeError(f"Unexpected status {response.status}")
            data = json.load(response)
            # Expecting a list of bounty dicts
            if not isinstance(data, list):
                raise ValueError("API did not return a list")
            return data
    except urllib.error.URLError as exc:
        logging.error(f"Failed to fetch bounty data: {exc}")
        raise

def format_bounty_entry(idx: int, bounty: Dict[str, Any]) -> str:
    """Return a markdown formatted line for a single bounty."""
    title = bounty.get("title", "Untitled")
    url = bounty.get("url", "#")
    repo = bounty.get("repository", "unknown")
    comments = bounty.get("comments", 0)
    updated = bounty.get("last_updated", "unknown")
    return (
        f"#### {idx}. [{title}]({url})\n"
        f"- **Repository:** [{repo}]({repo})\n"
        f"- **Comments:** {comments}\n"
        f"- **Last Updated:** {updated}\n"
    )

def build_issue_body(bounties: List[Dict[str, Any]]) -> str:
    """Construct the full markdown body for the issue."""
    header = (
        "### Active Bounty Scan Results\n\n"
        f"**Scan Time:** {bounties[0].get('scan_time', 'unknown')}\n\n"
    )
    entries = "\n".join(
        format_bounty_entry(i + 1, b) for i, b in enumerate(bounties[:MAX_BOUNTIES])
    )
    footer = "\n*This issue was generated automatically by the BountyScout workflow.*"
    return header + entries + footer

def github_request(method: str, endpoint: str, payload: Dict = None) -> Dict:
    """Perform a request against the GitHub REST API."""
    url = f"{GITHUB_API}{endpoint}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "BountyScout-Alert-Bot",
    }
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status >= 400:
                raise RuntimeError(f"GitHub API error {resp.status}")
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode()
        logging.error(f"GitHub API request failed: {exc.code} {body}")
        raise
    except urllib.error.URLError as exc:
        logging.error(f"Network error contacting GitHub API: {exc}")
        raise

def find_existing_alert_issue() -> Dict | None:
    """Search for an open issue whose title starts with the alert prefix."""
    query = f"repo:{REPO_OWNER}/{REPO_NAME} is:issue is:open in:title \"🎯 Bounty Alert\""
    endpoint = f"/search/issues?q={urllib.parse.quote(query)}"
    result = github_request("GET", endpoint)
    items = result.get("items", [])
    return items[0] if items else None

def create_or_update_issue(body: str):
    """Create a new alert issue or comment on an existing one."""
    existing = find_existing_alert_issue()
    title = "🎯 Bounty Alert: New Opportunities Detected"
    if existing:
        issue_number = existing["number"]
        comment_endpoint = f"/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}/comments"
        github_request("POST", comment_endpoint, {"body": body})
        logging.info(f"Added comment to existing alert issue #{issue_number}")
    else:
        create_endpoint = f"/repos/{REPO_OWNER}/{REPO_NAME}/issues"
        payload = {"title": title, "body": body, "labels": ["bounty", "automated"]}
        issue = github_request("POST", create_endpoint, payload)
        logging.info(f"Created new alert issue #{issue['number']}")

# --------------------------------------------------------------------------- #
# Main execution
# --------------------------------------------------------------------------- #
def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logging.info("Fetching active bounty data...")
    bounties = fetch_bounty_data(BOUNTY_API_URL)

    if not bounties:
        logging.info("No active bounties found – exiting.")
        return

    # Ensure each entry contains the fields we need; fill defaults if missing.
    for b in bounties:
        b.setdefault("title", "Untitled")
        b.setdefault("url", "#")
        b.setdefault("repository", "unknown")
        b.setdefault("comments", 0)
        b.setdefault("last_updated", "unknown")
        b.setdefault("scan_time", "unknown")

    body = build_issue_body(bounties)
    create_or_update_issue(body)


if __name__ == "__main__":
    main()

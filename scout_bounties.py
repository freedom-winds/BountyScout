
import json
import os
import urllib.request
import urllib.parse
import re
from datetime import datetime, timezone

# Configuration
STATE_FILE = "seen_bounties.json"
MAX_COMMENTS = 25 # Filter out overcrowded threads

# GitHub search queries for active bounty opportunities
SEARCH_QUERIES = [
    'is:issue is:open bounty in:title,body sort:updated-desc',
    'is:issue is:open reward bounty sort:updated-desc',
    'is:issue is:open "paid" "PR" "bounty" sort:updated-desc',
    'is:issue is:open "Opire" bounty sort:updated-desc',
]

def load_seen_bounties():
    """Load previously seen bounty URLs from the state file."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return set(data)
        except Exception as e:
            print(f"Error loading state file: {e}")
    return set()

def save_seen_bounties(seen_urls):
    """Save the updated list of seen bounty URLs."""
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(list(seen_urls), f, indent=2)
    except Exception as e:
        print(f"Error saving state file: {e}")

def search_github(query, token=None):
    """Fetch search results from GitHub Issues API."""
    url = f"https://api.github.com/search/issues?{urllib.parse.urlencode({'q': query, 'per_page': 15})}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "MyPersonalBountyScout",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"GitHub Search API Error for query '{query}': {e}")
        return {}

def is_clean_candidate(item):
    """Triage logic to filter out noisy, assigned, closed, or spam tasks."""
    # 1. Skip if already a Pull Request
    if "pull_request" in item:
        return False
    # 2. Skip if already assigned
    if item.get("assignees"):
        return False
    # 3. Skip if thread is overcrowded (highly competitive)
    if int(item.get("comments", 0)) > MAX_COMMENTS:
        return False
    
    title = str(item.get("title", "")).lower()
    body = str(item.get("body", "")).lower()
    
    # 4. Skip cryptocurrency/article writing/spam keywords
    blocklist = [
        "airdrop", "referral", "casino", "gambling", "trading bot", 
        "blog post", "article writing", "tutorial proposal", "content creator"
    ]
    if any(term in title or term in body for term in blocklist):
        return False
        
    return True

def send_telegram_notification(token, chat_id, message):
    """Send a notification message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print("Telegram notification sent successfully.")
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")

def send_discord_notification(webhook_url, message):
    """Send a notification message via Discord Webhook."""
    payload = {
        "content": message
    }
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print("Discord notification sent successfully.")
    except Exception as e:
        print(f"Failed to send Discord notification: {e}")

def create_github_issue(repo_fullname, token, title, body):
    """Create an issue in the host repository to trigger a native GitHub alert."""
    url = f"https://api.github.com/repos/{repo_fullname}/issues"
    payload = {
        "title": title,
        "body": body,
        "labels": ["bounty-alert"]
    }
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "MyPersonalBountyScout",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}"
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            print("GitHub Issue notification created successfully.")
    except Exception as e:
        print(f"Failed to create GitHub Issue: {e}")

def main():
    """
    Main function to scout for new bounties, filter them,
    and send notifications if new opportunities are found.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    github_repo_for_alerts = os.getenv("GITHUB_REPO_FOR_ALERTS") # e.g., "owner/repo"
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not github_token:
        print("Warning: GITHUB_TOKEN environment variable not set. GitHub search may be rate-limited.")
    if not github_repo_for_alerts:
        print("Warning: GITHUB_REPO_FOR_ALERTS environment variable not set. Cannot create GitHub issues.")

    seen_urls = load_seen_bounties()
    new_bounties = []
    current_active_urls = set() # To store all URLs found in this run, to update seen_bounties.json

    print("Starting bounty scout...")

    for query in SEARCH_QUERIES:
        print(f"Searching GitHub with query: '{query}'")
        search_results = search_github(query, github_token)
        if search_results:
            for item in search_results.get("items", []):
                url = item.get("html_url")
                if not url:
                    continue

                # Add all found URLs to current_active_urls, regardless if they are new or not.
                # This ensures that seen_bounties.json correctly reflects all *currently active* bounties,
                # preventing old, closed bounties from staying in the seen list indefinitely.
                current_active_urls.add(url)

                if url not in seen_urls and is_clean_candidate(item):
                    repo_name_full = item["repository_url"].replace("https://api.github.com/repos/", "")
                    new_bounties.append({
                        "title": item["title"],
                        "url": url,
                        "comments": item["comments"],
                        "repository": repo_name_full,
                        "repository_url": item["repository_url"].replace("api.", "").replace("/repos", "") # Convert API URL to browser URL
                    })
                    seen_urls.add(url) # Add to seen_urls immediately to avoid duplicates within the same run

    if new_bounties:
        print(f"Found {len(new_bounties)} new bounty opportunities!")
        
        # --- Prepare Notification Messages ---
        issue_title = f"🎯 Bounty Alert: {len(new_bounties)} New Opportunities found"
        issue_body_lines = ["**New GitHub Bounty Opportunities:**\n"]
        
        for i, bounty in enumerate(new_bounties):
            issue_body_lines.append(
                f"{i+1}. [{bounty['title']}]({bounty['url']}) - Comments: {bounty['comments']}\n"
                f"   Repository: [{bounty['repository']}]({bounty['repository_url']})"
            )
        issue_body = "\n".join(issue_body_lines)

        # Telegram markdown is slightly different, but for simplicity, we'll reuse the GitHub body.
        telegram_message = issue_body
        discord_message = issue_body

        # --- Send Notifications ---
        if github_repo_for_alerts and github_token:
            create_github_issue(github_repo_for_alerts, github_token, issue_title, issue_body)
        else:
            print("Skipping GitHub Issue creation: GITHUB_REPO_FOR_ALERTS or GITHUB_TOKEN not set.")

        if telegram_bot_token and telegram_chat_id:
            send_telegram_notification(telegram_bot_token, telegram_chat_id, telegram_message)
        else:
            print("Skipping Telegram notification: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set.")

        if discord_webhook_url:
            send_discord_notification(discord_webhook_url, discord_message)
        else:
            print("Skipping Discord notification: DISCORD_WEBHOOK_URL not set.")
    else:
        print("No new bounty opportunities found.")
    
    # Save the consolidated list of all active bounties (new and previously seen)
    # This prevents old, no longer active bounties from staying in the 'seen' list indefinitely.
    save_seen_bounties(current_active_urls)
    print("Bounty scout finished.")

if __name__ == "__main__":
    main()
    
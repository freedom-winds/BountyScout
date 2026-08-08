
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
        # Fix: Complete the print statement for the exception
        print(f"Failed to create GitHub Issue: {e}")

# Main execution logic for the bounty scout
def main():
    github_token = os.environ.get("GITHUB_TOKEN")
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    discord_webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    github_repo_fullname = os.environ.get("GITHUB_REPO_FULLNAME") # Format: "owner/repo"

    seen_bounties = load_seen_bounties()
    new_bounty_items = []

    for query in SEARCH_QUERIES:
        results = search_github(query, github_token)
        if results and "items" in results:
            for item in results["items"]:
                url = item["html_url"]
                # Only process if not seen and passes triage
                if url not in seen_bounties and is_clean_candidate(item):
                    new_bounty_items.append(item)
                    seen_bounties.add(url) # Add to seen *after* it's identified as new and clean

    if new_bounty_items:
        num_opportunities = len(new_bounty_items)
        # Fix: Correct "Opportunityies" to "Opportunities"
        title = f"🎯 Bounty Alert: {num_opportunities} New Opportunities found"
        
        body_lines = [title, ""]
        for bounty in new_bounty_items:
            # Extract relevant info for the notification body
            item_title = bounty.get("title", "No Title")
            item_url = bounty.get("html_url", "#")
            
            # Extract repository name from repository_url for better context
            repo_url_api = bounty.get("repository_url", "")
            repo_name = "Unknown Repo"
            if repo_url_api:
                # Example: https://api.github.com/repos/owner/repo -> owner/repo
                match = re.search(r'github\.com/repos/([^/]+/[^/]+)', repo_url_api)
                if match:
                    repo_name = match.group(1)
            
            # Format the body message for each bounty
            body_lines.append(f"- [{item_title}]({item_url}) in `{repo_name}`")
            
        body = "\n".join(body_lines)

        # Send notifications
        if github_repo_fullname and github_token:
            create_github_issue(github_repo_fullname, github_token, title, body)
        
        if telegram_token and telegram_chat_id:
            send_telegram_notification(telegram_token, telegram_chat_id, body)
        
        if discord_webhook_url:
            send_discord_notification(discord_webhook_url, body)
    else:
        print("No new bounty opportunities found.")

    # Save the updated list of seen bounties
    save_seen_bounties(seen_bounties)

if __name__ == "__main__":
    main()
    
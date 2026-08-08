
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
        print(f"Failed to create GitHub Issue: {e}") # <-- CHANGE: Completed the truncated print statement

# --- NEW CODE: Main execution logic and environment variable setup ---

# Environment variables for tokens and IDs
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
# The repository where the issue should be created (e.g., "owner/repo")
GITHUB_REPO_FULLNAME = os.getenv("GITHUB_REPO_FULLNAME")

def main():
    print("Starting bounty scout...")
    
    seen_bounties = load_seen_bounties()
    new_opportunities = []
    
    for query in SEARCH_QUERIES:
        print(f"\nSearching GitHub with query: '{query}'")
        results = search_github(query, GITHUB_TOKEN)
        
        if results and "items" in results:
            for item in results["items"]:
                item_url = item.get("html_url")
                if not item_url:
                    continue # Skip if no URL
                
                if item_url not in seen_bounties:
                    if is_clean_candidate(item):
                        new_opportunities.append({
                            "title": item.get("title"),
                            "url": item_url
                        })
                        seen_bounties.add(item_url)
                        print(f"  Found new opportunity: {item.get('title')} - {item_url}")
        else:
            print(f"  No items found or error in search for query: '{query}'")

    if new_opportunities:
        num_new = len(new_opportunities)
        # Correcting "Opportunityies" to "Opportunities" for the alert title
        alert_title = f"🎯 Bounty Alert: {num_new} New Opportunit{'y' if num_new == 1 else 'ies'} Found!"
        
        alert_message_base = f"Hey there! I've sniffed out {num_new} potential new bounty opportunities for you:\n\n"
        for i, op in enumerate(new_opportunities):
            alert_message_base += f"- [{op['title']}]({op['url']})\n"
        
        print(f"\n--- {alert_title} ---")
        print(alert_message_base)

        # GitHub Issue Notification
        if GITHUB_REPO_FULLNAME and GITHUB_TOKEN:
            print("\nAttempting to create GitHub Issue...")
            create_github_issue(GITHUB_REPO_FULLNAME, GITHUB_TOKEN, alert_title, alert_message_base)
        else:
            print("\nSkipping GitHub Issue notification: GITHUB_REPO_FULLNAME or GITHUB_TOKEN not set.")

        # Telegram Notification
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            print("\nAttempting to send Telegram notification...")
            send_telegram_notification(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, alert_message_base)
        else:
            print("\nSkipping Telegram notification: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set.")

        # Discord Notification
        if DISCORD_WEBHOOK_URL:
            print("\nAttempting to send Discord notification...")
            send_discord_notification(DISCORD_WEBHOOK_URL, alert_message_base)
        else:
            print("\nSkipping Discord notification: DISCORD_WEBHOOK_URL not set.")
            
    else:
        print("\nNo new bounty opportunities found.")
        
    save_seen_bounties(seen_bounties)
    print("\nBounty scout finished.")

if __name__ == "__main__":
    main()
    
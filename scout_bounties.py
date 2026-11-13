
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
    Main function to orchestrate the bounty scouting process.
    It loads previously seen bounties, searches GitHub for new opportunities,
    filters them, sends notifications, and updates the seen bounties list.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    github_repo_fullname = os.getenv("GITHUB_REPO_FULLNAME") # e.g., "owner/repo"

    if not github_token:
        print("WARNING: GITHUB_TOKEN environment variable not set. GitHub API calls may be rate-limited, and issue creation will fail.")

    seen_urls = load_seen_bounties()
    new_bounties_found = []

    for query in SEARCH_QUERIES:
        print(f"Searching GitHub with query: '{query}'...")
        results = search_github(query, github_token)
        if results and 'items' in results:
            for item in results['items']:
                item_url = item.get('html_url')
                if item_url and item_url not in seen_urls:
                    if is_clean_candidate(item):
                        new_bounties_found.append({
                            'title': item.get('title'),
                            'url': item_url,
                            'comments': item.get('comments', 0)
                        })
                        seen_urls.add(item_url)
                        print(f"  -> Found new bounty: {item.get('title')} - {item_url}")
        else:
            print(f"  -> No items found for query '{query}' or API error occurred.")

    if new_bounties_found:
        print(f"\nTotal new bounties found: {len(new_bounties_found)}")
        
        # Prepare notification message
        alert_title = f"🎯 Bounty Alert: {len(new_bounties_found)} New Opportunit{'y' if len(new_bounties_found) == 1 else 'ies'} found"
        
        notification_body = f"Hello! I've scouted some new bounty opportunities for you:\n\n"
        github_issue_body = f"Hello! I've scouted some new bounty opportunities for you:\n\n"

        for bounty in new_bounties_found:
            bounty_line = f"- [{bounty['title']}]({bounty['url']}) (Comments: {bounty['comments']})\n"
            notification_body += bounty_line
            github_issue_body += bounty_line
        
        notification_body += "\nGood luck hunting! 🚀"
        github_issue_body += "\nGood luck hunting! 🚀"

        # Send Telegram notification
        if telegram_bot_token and telegram_chat_id:
            send_telegram_notification(telegram_bot_token, telegram_chat_id, notification_body)
        else:
            print("Telegram credentials not fully set. Skipping Telegram notification.")

        # Send Discord notification
        if discord_webhook_url:
            send_discord_notification(discord_webhook_url, notification_body)
        else:
            print("Discord webhook URL not set. Skipping Discord notification.")

        # Create GitHub Issue
        if github_repo_fullname and github_token:
            create_github_issue(github_repo_fullname, github_token, alert_title, github_issue_body)
        else:
            print("GitHub repository full name or GITHUB_TOKEN not set. Skipping GitHub issue creation.")
            
    else:
        print("No new bounty opportunities found this run.")

    save_seen_bounties(seen_urls)
    print("Bounty scouting complete.")

if __name__ == "__main__":
    main()
    
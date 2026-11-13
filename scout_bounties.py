
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
    """Main function to scout for bounties and send notifications."""
    github_token = os.getenv("GITHUB_TOKEN")
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    repo_fullname = os.getenv("GITHUB_REPOSITORY") # e.g., "owner/repo" - crucial for creating issue

    if not github_token:
        print("WARNING: GITHUB_TOKEN environment variable not set. GitHub search and issue creation might be limited or fail.")
    if not repo_fullname:
        print("WARNING: GITHUB_REPOSITORY environment variable not set. GitHub issue creation will fail.")

    seen_urls = load_seen_bounties()
    new_bounties = []

    print(f"Starting bounty scout at {datetime.now(timezone.utc).isoformat()}")
    print(f"Currently tracking {len(seen_urls)} seen bounties.")

    for query in SEARCH_QUERIES:
        print(f"Searching GitHub with query: '{query}'")
        results = search_github(query, github_token)
        if results and "items" in results:
            for item in results["items"]:
                issue_url = item.get("html_url")
                if issue_url and issue_url not in seen_urls:
                    if is_clean_candidate(item):
                        new_bounties.append(item)
                        seen_urls.add(issue_url)
                        print(f"Found new clean bounty: {item.get('title')} ({issue_url})")
                    # else: # Optional: print why a candidate was skipped
                    #     print(f"Skipping non-clean candidate: {item.get('title')} ({issue_url})")
                # elif issue_url and issue_url in seen_urls: # Optional: print already seen
                #     print(f"Skipping already seen bounty: {item.get('title')} ({issue_url})")
        else:
            print(f"No items found for query '{query}' or API error.")

    if new_bounties:
        notification_title = f"🎯 Bounty Alert: {len(new_bounties)} New Opportunit{'y' if len(new_bounties) == 1 else 'ies'} Found!"
        notification_body_parts = [
            f"Hey there! Found some new bounty opportunities for you:\n"
        ]
        for bounty in new_bounties:
            title = bounty.get("title", "No Title")
            url = bounty.get("html_url", "#")
            repo_url_parts = url.split('/')
            # Assuming format like https://github.com/owner/repo/issues/123
            repo_link = f"https://github.com/{repo_url_parts[3]}/{repo_url_parts[4]}" if len(repo_url_parts) > 4 else "#"
            notification_body_parts.append(f"- **[{title}]({url})** in [{repo_url_parts[3]}/{repo_url_parts[4]}]({repo_link})")
        notification_body_parts.append("\nGo get 'em!")
        notification_body = "\n".join(notification_body_parts)

        print(notification_title)
        print(notification_body)

        # Create GitHub Issue
        if repo_fullname and github_token:
            print(f"Attempting to create GitHub issue in {repo_fullname}...")
            create_github_issue(repo_fullname, github_token, notification_title, notification_body)
        else:
            print("Skipping GitHub issue creation: GITHUB_REPOSITORY or GITHUB_TOKEN not set.")

        # Send Telegram Notification
        if telegram_bot_token and telegram_chat_id:
            print("Attempting to send Telegram notification...")
            send_telegram_notification(telegram_bot_token, telegram_chat_id, notification_body)
        else:
            print("Skipping Telegram notification: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set.")

        # Send Discord Notification
        if discord_webhook_url:
            print("Attempting to send Discord notification...")
            send_discord_notification(discord_webhook_url, notification_body)
        else:
            print("Skipping Discord notification: DISCORD_WEBHOOK_URL not set.")
    else:
        print("No new bounties found this run.")

    save_seen_bounties(seen_urls)
    print("Bounty scout finished.")

if __name__ == "__main__":
    main()

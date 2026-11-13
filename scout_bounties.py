
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
    github_token = os.environ.get("GITHUB_TOKEN")
    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    discord_webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    github_repo_fullname = os.environ.get("GITHUB_REPOSITORY") # e.g., "owner/repo_name"

    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set. Cannot proceed.")
        return

    seen_urls = load_seen_bounties()
    new_bounties = []

    print("Starting bounty scout...")

    for query in SEARCH_QUERIES:
        print(f"Searching GitHub with query: {query}")
        results = search_github(query, github_token)
        if results and "items" in results:
            for item in results["items"]:
                issue_url = item.get("html_url")
                if issue_url and issue_url not in seen_urls and is_clean_candidate(item):
                    new_bounties.append(item)
                    seen_urls.add(issue_url)
                    print(f"Found new bounty: {item.get('title')} - {issue_url}")
        else:
            print(f"No items found for query: {query}")

    if new_bounties:
        num_new_bounties = len(new_bounties)
        issue_title = f"🎯 Bounty Alert: {num_new_bounties} New Opportunit{'y' if num_new_bounties == 1 else 'ies'} found"
        
        issue_body_parts = [
            f"Hey team, I've scouted {num_new_bounties} new potential bounty opportunities for you!",
            "---",
        ]
        
        for bounty in new_bounties:
            title = bounty.get("title", "No Title")
            url = bounty.get("html_url", "#")
            repo_url_raw = bounty.get("repository_url", "")
            repo_url = repo_url_raw.replace("api.github.com/repos", "github.com") if repo_url_raw else "#"
            repo_name = repo_url.split('/')[-1] if '/' in repo_url else "Unknown Repo"
            comments = bounty.get("comments", 0)
            updated_at_str = bounty.get("updated_at")
            
            updated_info = ""
            if updated_at_str:
                try:
                    updated_dt = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
                    time_ago = datetime.now(timezone.utc) - updated_dt
                    days_ago = time_ago.days
                    if days_ago == 0:
                        updated_info = "(updated today)"
                    elif days_ago == 1:
                        updated_info = "(updated yesterday)"
                    else:
                        updated_info = f"(updated {days_ago} days ago)"
                except ValueError:
                    pass

            issue_body_parts.append(
                f"- **[{title}]({url})** in [{repo_name}]({repo_url}) {updated_info} ({comments} comments)"
            )
        issue_body_parts.append("---")
        issue_body_parts.append("Happy hunting! 🚀")
        
        issue_body = "\n".join(issue_body_parts)

        print(f"Preparing GitHub issue: {issue_title}")
        if github_repo_fullname:
            create_github_issue(github_repo_fullname, github_token, issue_title, issue_body)
        else:
            print("Warning: GITHUB_REPOSITORY environment variable not set. Skipping GitHub issue creation.")

        if telegram_bot_token and telegram_chat_id:
            print("Sending Telegram notification...")
            send_telegram_notification(telegram_bot_token, telegram_chat_id, issue_body)
        else:
            print("Telegram credentials not fully set. Skipping Telegram notification.")

        if discord_webhook_url:
            print("Sending Discord notification...")
            send_discord_notification(discord_webhook_url, issue_body)
        else:
            print("Discord webhook URL not set. Skipping Discord notification.")
    else:
        print("No new bounties found.")

    save_seen_bounties(seen_urls)
    print("Bounty scout finished.")

if __name__ == "__main__":
    main()
    
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
        print(f"Failed to create GitHub issue: {e}")

def main():
    """Main entry point for the bounty scout workflow."""
    seen_urls = load_seen_bounties()
    active_issues = []
    
    # Iterate through search queries
    for query in SEARCH_QUERIES:
        try:
            print(f"Searching with query: {query[:50]}...")
            response_data = search_github(query)
            if not response_data or "items" not in response_data:
                continue
            
            items = response_data.get("items", [])
            # Process first page of results (GitHub search limits per query usually)
            for item in items:
                url = item.get("html_url", "")
                seen_urls.discard(url) # Remove from seen if it wasn't actually seen before this run
                
                if is_clean_candidate(item):
                    # Collect new bounty details
                    repo_name = item.get("repository", {}).get("full_name", "Unknown")
                    title = item.get("title", "No Title")[:50] + "..." if len(item.get("title","")) > 50 else item.get("title", "No Title")
                    body_snippet = item.get("body", "")[:200]
                    
                    # Construct alert message
                    msg = f"🎯 *Bounty Opportunity Found*\n\n*Repository*: {repo_name}\n*Issue ID*: #{item.get('number', 'Unknown')}\n*Title*: {title}\n*Link*: {url}\n---\n*Description*: {body_snippet}"
                    
                    # Update seen set to track processed
                    seen_urls.add(url)
                    active_issues.append({"url": url, "repo": repo_name})
                
                # Optionally create issue (commented out by default to avoid spamming own repo unless configured)
                # if os.environ.get("AUTO_CREATE_ISSUE") == "true":
                #     create_github_issue(item.get('repository', {}).get('full_name'), os.environ.get('GITHUB_TOKEN'), title, body_snippet)
                    
        except Exception as search_err:
            print(f"Error during search iteration: {search_err}")
    
    # Save state to disk
    save_seen_bounties(seen_urls)
    
    if active_issues:
        print(f"Discovered {len(active_issues)} new potential bounties.")
        # Send notifications if environment variables are set
        try:
            telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
            chat_id = os.environ.get("TELEGRAM_CHAT_ID")
            if telegram_token and chat_id:
                msg = f"🎯 *Bounty Alert Scan Report*\n\nFound {len(active_issues)} new opportunities.\nSee logs for details."
                send_telegram_notification(telegram_token, chat_id, msg)
        except Exception as te_err:
            print(f"Telegram Notification Failed: {te_err}")
    
    else:
        print("No new clean bounties found in this scan run.")

if __name__ == "__main__":
    main()

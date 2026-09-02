"""Automated GitHub bounty scanner and multi-channel notification dispatcher."""

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone

STATE_FILE = "seen_bounties.json"
MAX_COMMENTS = 25

SEARCH_QUERIES = [
    'is:issue is:open bounty in:title,body sort:updated-desc',
    'is:issue is:open reward bounty sort:updated-desc',
    'is:issue is:open "paid" "PR" "bounty" sort:updated-desc',
    'is:issue is:open "Opire" bounty sort:updated-desc',
]

SPAM_BLOCKLIST = [
    "airdrop",
    "referral",
    "casino",
    "gambling",
    "trading bot",
    "blog post",
    "article writing",
    "tutorial proposal",
    "content creator",
    "faucet",
    "giveaway",
    "retweet",
]


def pluralize_opportunity(count: int, capitalize: bool = False) -> str:
    """Return correct singular or plural form of opportunity.

    Args:
        count (int): Number of discovered opportunities.
        capitalize (bool): Whether to capitalize the first letter.

    Returns:
        str: Formatted opportunity word.
    """
    if count == 1:
        return "Opportunity" if capitalize else "opportunity"
    return "Opportunities" if capitalize else "opportunities"


def load_seen_bounties(state_file: str = STATE_FILE) -> set:
    """Load previously seen bounty URLs from the state file.

    Args:
        state_file (str): Path to the state file.

    Returns:
        set: Set of seen bounty URL strings.
    """
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return set(data)
        except Exception as e:
            print(f"Error loading state file: {e}")
    return set()


def save_seen_bounties(seen_urls: set, state_file: str = STATE_FILE) -> None:
    """Save the updated list of seen bounty URLs.

    Args:
        seen_urls (set): Set of seen bounty URL strings.
        state_file (str): Path to the state file.

    Returns:
        None
    """
    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(sorted(list(seen_urls)), f, indent=2)
    except Exception as e:
        print(f"Error saving state file: {e}")


def search_github(query: str, token: str = None) -> dict:
    """Fetch search results from GitHub Issues API.

    Args:
        query (str): GitHub search query string.
        token (str, optional): GitHub personal access token.

    Returns:
        dict: Parsed JSON response payload from the GitHub Search API.
    """
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


def is_clean_candidate(item: dict, current_repo: str = None) -> bool:
    """Triage logic to filter out noisy, assigned, closed, recursive, or spam tasks.

    Args:
        item (dict): Issue payload item from the GitHub API.
        current_repo (str, optional): Current repository name formatted as 'owner/repo'.

    Returns:
        bool: True if the issue is a clean, qualified candidate; False otherwise.
    """
    if not isinstance(item, dict):
        return False

    if item.get("state") == "closed":
        return False

    if item.get("locked") is True:
        return False

    if "pull_request" in item and item["pull_request"]:
        return False

    if item.get("assignees") or item.get("assignee"):
        return False

    comments_count = item.get("comments")
    if comments_count is not None:
        try:
            if int(comments_count) > MAX_COMMENTS:
                return False
        except (ValueError, TypeError):
            pass

    url = str(item.get("html_url") or "")
    title = str(item.get("title") or "").strip()
    title_lower = title.lower()
    body = str(item.get("body") or "").lower()

    if current_repo and current_repo.lower() in url.lower():
        return False

    repo_part = url.split("/issues/")[0].lower() if "/issues/" in url else url.lower()
    if "bountyscout" in repo_part or "bounty-scout" in repo_part:
        return False

    if "bounty alert:" in title_lower or "🎯 bounty alert" in title_lower or title_lower.startswith("bounty alert"):
        return False

    if any(term in title_lower or term in body for term in SPAM_BLOCKLIST):
        return False

    return True


def format_notification_message(new_bounties: list, now_str: str) -> str:
    """Format Telegram and Discord markdown notification message with proper pluralization.

    Args:
        new_bounties (list): List of new bounty dictionaries.
        now_str (str): Formatted timestamp string.

    Returns:
        str: Formatted markdown notification string.
    """
    count = len(new_bounties)
    plural_word = pluralize_opportunity(count, capitalize=False)
    notif_lines = [
        f"🎯 *New Bounty Alert* ({now_str})",
        f"Found {count} new {plural_word}:\n",
    ]
    for idx, b in enumerate(new_bounties, start=1):
        notif_lines.append(f"{idx}. *{b['title']}*")
        notif_lines.append(f"   • Repository: `{b['repo']}`")
        notif_lines.append(f"   • Comments: {b['comments']}")
        notif_lines.append(f"   • Link: {b['url']}\n")

    return "\n".join(notif_lines)


build_notification_markdown = format_notification_message


def format_github_issue_content(new_bounties: list, now_str: str) -> tuple:
    """Format GitHub Issue title and body with proper pluralization.

    Args:
        new_bounties (list): List of new bounty dictionaries.
        now_str (str): Formatted timestamp string.

    Returns:
        tuple: (issue_title, issue_body)
    """
    count = len(new_bounties)
    plural_word = pluralize_opportunity(count, capitalize=True)
    issue_title = f"🎯 Bounty Alert: {count} New {plural_word} found"
    issue_body_lines = [
        "### Active Bounty Scan Results\n\n",
        f"**Scan Time:** {now_str}\n\n",
    ]
    for idx, b in enumerate(new_bounties, start=1):
        issue_body_lines.append(
            f"#### {idx}. [{b['title']}]({b['url']})\n"
            f"- **Repository:** [{b['repo']}](https://github.com/{b['repo']})\n"
            f"- **Comments:** {b['comments']}\n"
            f"- **Last Updated:** {b['updated_at']}\n\n"
        )
    return issue_title, "".join(issue_body_lines)


build_github_issue_payload = format_github_issue_content


def send_telegram_notification(token: str, chat_id: str, message: str) -> None:
    """Send a notification message via Telegram Bot API.

    Args:
        token (str): Telegram Bot API token.
        chat_id (str): Target Telegram chat ID.
        message (str): Markdown formatted message.

    Returns:
        None
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print("Telegram notification sent successfully.")
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")


def send_discord_notification(webhook_url: str, message: str) -> None:
    """Send a notification message via Discord Webhook.

    Args:
        webhook_url (str): Target Discord webhook URL.
        message (str): Plain or markdown formatted message content.

    Returns:
        None
    """
    payload = {"content": message}
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print("Discord notification sent successfully.")
    except Exception as e:
        print(f"Failed to send Discord notification: {e}")


def create_github_issue(repo_fullname: str, token: str, title: str, body: str) -> None:
    """Create an issue in the host repository to trigger a native GitHub alert.

    Args:
        repo_fullname (str): Full name of repository 'owner/repo'.
        token (str): GitHub token.
        title (str): Issue title.
        body (str): Issue body markdown.

    Returns:
        None
    """
    url = f"https://api.github.com/repos/{repo_fullname}/issues"
    payload = {
        "title": title,
        "body": body,
        "labels": ["bounty-alert"],
    }
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "MyPersonalBountyScout",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            print("GitHub Issue notification created successfully.")
    except Exception as e:
        print(f"Failed to create GitHub Issue notification: {e}")


def main() -> None:
    """Execute the primary scouting cycle and dispatch notifications."""
    github_token = os.environ.get("GITHUB_TOKEN")
    repo_fullname = os.environ.get("GITHUB_REPOSITORY")

    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    discord_webhook = os.environ.get("DISCORD_WEBHOOK_URL")

    seen_urls = load_seen_bounties()
    new_bounties = []

    print("Scouting GitHub for active bounties...")
    for query in SEARCH_QUERIES:
        results = search_github(query, github_token)
        for item in results.get("items", []):
            url = item.get("html_url")
            if url and url not in seen_urls:
                if is_clean_candidate(item, current_repo=repo_fullname):
                    new_bounties.append({
                        "title": item.get("title"),
                        "url": url,
                        "repo": url.split("/issues/")[0].replace("https://github.com/", ""),
                        "comments": item.get("comments", 0),
                        "updated_at": item.get("updated_at", ""),
                    })
                    seen_urls.add(url)

    if not new_bounties:
        print("No new bounty opportunities found.")
        return

    print(f"Discovered {len(new_bounties)} NEW bounty opportunities!")

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    notification_msg = format_notification_message(new_bounties, now_str)

    if telegram_token and telegram_chat_id:
        send_telegram_notification(telegram_token, telegram_chat_id, notification_msg)

    if discord_webhook:
        discord_msg = notification_msg.replace("•", "-")
        send_discord_notification(discord_webhook, discord_msg)

    if github_token and repo_fullname:
        issue_title, issue_body = format_github_issue_content(new_bounties, now_str)
        create_github_issue(repo_fullname, github_token, issue_title, issue_body)

    save_seen_bounties(seen_urls)
    print("State saved successfully.")


if __name__ == "__main__":
    main()

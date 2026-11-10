def format_bounty_alert_title(count: int) -> str:
    """
    Format the title for bounty alert issues with correct grammar and pluralization.

    Args:
        count: The number of new opportunities found.

    Returns:
        Formatted issue title string.
    """
    word = "Opportunity" if count == 1 else "Opportunities"
    return f"🎯 Bounty Alert: {count} New {word} found"

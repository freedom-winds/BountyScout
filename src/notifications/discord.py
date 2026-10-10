import os
from typing import Optional

import httpx

from src.config import settings


WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", settings.DISCORD_WEBHOOK_URL)


async def send_discord_alert(message: str) -> None:
    """Send a bounty alert to Discord via webhook."""
    if not WEBHOOK_URL:
        return

    # Truncate message to Discord's 2000 char limit
    truncated = message[:1997] + "..." if len(message) > 2000 else message

    embed = {
        "title": "🎯 New Bounty Opportunities Found",
        "description": truncated,
        "color": 0xFFD700,
        "timestamp": "now",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            WEBHOOK_URL,
            json={"embeds": [embed]},
            timeout=10.0,
        )
        response.raise_for_status()

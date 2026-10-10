import os
from typing import Optional

import httpx

from src.config import settings


BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", settings.TELEGRAM_BOT_TOKEN)
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", settings.TELEGRAM_CHAT_ID)


async def send_telegram_alert(message: str) -> None:
    """Send a bounty alert to Telegram via Bot API."""
    if not BOT_TOKEN or not CHAT_ID:
        return

    # Telegram has a 4096 char limit for messages
    truncated = message[:4093] + "..." if len(message) > 4096 else message

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": truncated,
        "parse_mode": "Markdown",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=10.0)
        response.raise_for_status()

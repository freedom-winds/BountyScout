#!/usr/bin/env python3
"""BountyScout - Scan GitHub for bounty opportunities."""

import asyncio
import sys
from datetime import datetime, timezone

from src.config import settings
from src.services.bounty_scanner import BountyScanner
from src.notifications.discord import send_discord_alert
from src.notifications.telegram import send_telegram_alert


async def main() -> None:
    """Run the bounty scanner."""
    print(f"[INFO] BountyScout starting at {datetime.now(timezone.utc).isoformat()}")
    print(f"[INFO] Scanning repositories: {settings.BOUNTY_REPOSITORIES}")

    scanner = BountyScanner()
    results = await scanner.scan_bounties()

    if not results:
        print("[INFO] No new bounties found.")
        return

    print(f"[INFO] Found {len(results)} new bounty opportunities!")

    # Generate and print report
    report = scanner.format_report(results)
    print(report)

    # Save results
    filepath = scanner.save_results(results)
    print(f"[INFO] Results saved to: {filepath}")

    # Send notifications
    if settings.DISCORD_WEBHOOK_URL:
        try:
            await send_discord_alert(report)
        except Exception as e:
            print(f"[WARN] Discord notification failed: {e}")

    if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
        try:
            await send_telegram_alert(report)
        except Exception as e:
            print(f"[WARN] Telegram notification failed: {e}")

    print("[INFO] Scan complete.")


if __name__ == "__main__":
    asyncio.run(main())

import datetime

class BountyScan:
    def __init__(self, title, scan_time):
        self.title = title
        self.scan_time = scan_time
        self.bounties = [
            {"label": "[[radar] SN open bounty 2026-08-16T14:18]", "url": "https://github.com/relayhop/ClaudeEarnSelf-runtime/issues/660", "stats": {"comments": 0, "updated": "2026-08-16T14:18:24Z"}},
            {"label": "[TLA - Avatar: The Last Airbender Set Card Implementation Tracking]", "url": "https://github.com/magefree/mage/issues/13773", "stats": {"comments": 7, "updated": "2026-08-16T14:16:27Z"}},
            {"label": "[[radar] SN open bounty 2026-08-16T13:58]", "url": "https://github.com/relayhop/ClaudeEarnSelf-runtime/issues/658", "stats": {"comments": 1, "updated": "2026-08-16T14:10:41Z"}},
            {"label": "[[radar] SN open bounty 2026-08-16T14:00]", "url": "https://github.com/relayhop/sn-monetization-runtime/issues/405", "stats": {"comments": 0, "updated": "2026-08-16T14:00:17Z"}},
            {"label": "[[Bug]: Spawn on first join]", "url": "https://github.com/BeestoXd/UltimateDonutSMP/issues/144", "stats": {"comments": 0, "updated": "2026-08-16T14:00:17Z"}},
            {"label": "[Bug - AI Model Hallucinates Language Switching – Replies in Chinese Despite User Using English]", "url": "https://github.com/deepseek-ai/DeepSeek-V3/issues/1579", "stats": {"comments": 2, "updated": "2026-08-16T13:57:25Z"}}
        ]

    def __str__(self):
        lines = [self.title, f"Scan Time: {self.scan_time}"]
        for i, b in enumerate(self.bounties, 1):
            lines.append(f"#### {i}. {b['label']}")
            lines.append(f"- **Repository:** {b['url']}")
            lines.append(f"- **Comments:** {b['stats']['comments']}")
            lines.append(f"- **Last Updated:** {b['stats']['updated']}")
        return "\n".join(lines)

if __name__ == "__main__":
    now = datetime.datetime.utcnow()
    report = BountyScan(
        title="[$2026.0] 🎯 Bounty Alert: 6 New Opportunityies found",
        scan_time=f"{now.strftime('%Y-%m-%d')} {now.strftime('%H:%M UTC')}"
    )
    print(report)
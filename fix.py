class Bounty:
    def __init__(self, title, repo, comments, updated):
        self.title = title
        self.repo = repo
        self.comments = comments
        self.updated = updated

class ActiveScan:
    def __init__(self, name, time):
        self.name = name
        self.time = time
        self.collection = []

    def add(self, bounty):
        self.collection.append(bounty)

    def __str__(self):
        s = f"Title: [{self.name}]\n"
        s += f"**Scan Time:** {self.time}\n\n#### Active Bounty Scan Results\n"
        for i, b in enumerate(self.collection, 1):
            s += f"#### {i}. [{b.title}]\n"
            s += f"- **Repository:** [{b.repo}]\n"
            s += f"- **Comments:** {b.comments}\n"
            s += f"- **Last Updated:** {b.updated}\n"
            if i < len(self.collection):
                s += "\n"
        return s

if __name__ == "__main__":
    report = ActiveScan(
        "$2026.0 🎯 Bounty Alert: 6 New Opportunityies found",
        "2026-08-16 11:17 UTC"
    )

    report.add(Bounty(
        "[[radar] SN open bounty 2026-08-16T11:15]",
        "relayhop/ClaudeEarnSelf-runtime",
        0,
        "2026-08-16T11:15:48Z"
    ))

    report.add(Bounty(
        "Avatar's blanket unoptimized prop defeats Next.js image optimization for every avatar in the app",
        "MergeFi/frontend",
        1,
        "2026-08-16T11:13:22Z"
    ))

    report.add(Bounty(
        "[[radar] SN open bounty 2026-08-16T10:58]",
        "relayhop/ClaudeEarnSelf-runtime",
        0,
        "2026-08-16T10:58:09Z"
    ))

    report.add(Bounty(
        "[[radar] SN open bounty 2026-08-16T10:51]",
        "relayhop/sn-monetization-runtime",
        0,
        "2026-08-16T10:51:05Z"
    ))

    report.add(Bounty(
        "Desktop AppImage tries to connect to Tor without asking; no way to disable it (JIO/India ISP blocks Tor)",
        "vitorpamplona/amethyst",
        0,
        "2026-08-16T10:48:01Z"
    ))

    report.add(Bounty(
        "ZM needs a websocket",
        "ZoneMinder/zoneminder",
        10,
        "2026-08-16T10:33:18Z"
    ))

    print(report)
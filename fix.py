from dataclasses import dataclass

@dataclass
class BountyItem:
    index: int
    title: str
    repo: str
    comments: int
    updated: str

    def format_entry(self):
        return f"#### {self.index}. [{self.title}]\n" \
               f"- **Repository:** [{self.repo}]\n" \
               f"- **Comments:** {self.comments}\n" \
               f"- **Last Updated:** {self.updated}"

@dataclass
class ActiveScan:
    scan_time: str
    items: list

    def generate(self):
        output = f"## Active Bounty Scan Results\n\n**Scan Time:** {self.scan_time}\n\n"
        for b in self.items:
            output += b.format_entry()
        return output

def main():
    s = ActiveScan(
        scan_time="2026-08-17 04:38 UTC",
        items=[
            BountyItem(1, "[radar] SN open bounty 2026-08-17T04:25", "relayhop/sn-monetization-runtime", 0, "2026-08-17T04:25:56Z"),
            BountyItem(2, "🚨 Bounty Governo — Protezione civile e resilienza", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:25:26Z"),
            BountyItem(3, "📊 Bounty Governo — Trasparenza e dati pubblici", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:25:20Z"),
            BountyItem(4, "♿ Bounty Governo — Accessibilità e inclusione", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:25:15Z"),
            BountyItem(5, "🎓 Bounty Governo — Istruzione e formazione", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:25:12Z"),
            BountyItem(6, "🏥 Bounty Governo — Sanità e servizi al cittadino", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:25:08Z"),
            BountyItem(7, "🚆 Bounty Governo — Mobilità e infrastrutture", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:25:00Z"),
            BountyItem(8, "🌱 Bounty Governo — Ambiente, energia e sostenibilità", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:24:56Z"),
            BountyItem(9, "🔐 Bounty Governo — Cybersecurity e sicurezza dei servizi", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:24:48Z"),
            BountyItem(10, "💻 Bounty Governo — Digitalizzazione e interoperabilità", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:24:44Z"),
            BountyItem(11, "🏛️ Bounty Governo — Servizi pubblici e semplificazione", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:24:35Z"),
            BountyItem(12, "🤝 Bounty Urban Lab — Partecipazione civica e inclusione", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:20:48Z"),
            BountyItem(13, "🌱 Bounty Urban Lab — Verde, sostenibilità e resilienza urbana", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:20:44Z"),
            BountyItem(14, "🏙️ Bounty Urban Lab — Rigenerazione e spazio pubblico", "MyZubster-Ecosystem/myzubster", 0, "2026-08-17T04:20:39Z"),
        ]
    )
    print(s.generate())

if __name__ == "__main__":
    main()
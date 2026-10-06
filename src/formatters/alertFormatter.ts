import type { BountyAlert } from "../types/index.js";

export function formatBountyAlerts(alerts: BountyAlert[]): string {
  if (alerts.length === 0) {
    return "No new bounty opportunities found.";
  }

  const lines: string[] = [];
  lines.push(
    `🎯 Bounty Alert: ${alerts.length} New Opportunity${alerts.length > 1 ? "ies" : "y"} found`,
  );
  lines.push(`**Scan Time:** ${new Date().toISOString().replace("Z", " UTC")}`);
  lines.push("");
  lines.push("### Active Bounty Scan Results");
  lines.push("");

  alerts.forEach((alert, index) => {
    lines.push(
      `#### ${index + 1}. [${alert.title}](${alert.url})`,
    );
    lines.push(`- **Repository:** [${alert.repository}](${alert.url})`);
    lines.push(`- **Comments:** ${alert.comments}`);
    lines.push(`- **Last Updated:** ${alert.lastUpdated}`);
    lines.push("");
  });

  return lines.join("\n");
}

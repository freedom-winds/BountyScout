// Copyright 2026 Freedom Winds. All rights reserved.
import { Bounty } from "../types/bounty";
import { sendEmail } from "../utils/email";
import { getMaintainerEmail } from "../utils/github";

/**
 * Notifies repository maintainers about new bounty opportunities.
 * @param bounties - Array of newly inserted bounties.
 */
export const notifyMaintainers = async (bounties: Bounty[]): Promise<void> => {
  for (const bounty of bounties) {
    if (bounty.maintainer_alert_sent) continue;

    const maintainerEmail = await getMaintainerEmail(bounty.repository);
    if (!maintainerEmail) continue;

    await sendEmail({
      to: maintainerEmail,
      subject: `New Bounty Opportunity: ${bounty.title}`,
      html: generateNotificationEmail(bounty),
    });
  }
};

/**
 * Generates HTML content for the bounty notification email.
 */
const generateNotificationEmail = (bounty: Bounty): string => {
  return `<div>
    <h2>New Bounty Opportunity</h2>
    <p><strong>Repository:</strong> ${bounty.repository}</p>
    <p><strong>Issue:</strong> <a href="${bounty.issue_url}">${bounty.title}</a></p>
    <p><strong>Comments:</strong> ${bounty.comments}</p>
    <p><strong>Last Updated:</strong> ${new Date(bounty.last_updated).toLocaleString()}</p>
    <p>
      This issue has been identified as a potential bounty opportunity. 
      If you are the maintainer, please review and claim it via the <a href="https://bountyscout.freedom-winds.org">BountyScout platform</a>.
    </p>
  </div>`;
};

/**
 * Mock: Fetches maintainer email for a repository (placeholder for real implementation).
 */
export const getMaintainerEmail = async (repository: string): Promise<string | null> => {
  const maintainerMap: Record<string, string> = {
    "woahwhattheheck/commons": "maintainer@woahwhattheheck.org",
    "MentorsMind/MentorsMind-Contract": "dev@mentorsmind.org",
    "CitrateNetwork/citrate-cluster": "security@citrate.network",
    "degenspot/BACKit-onStellar": "bounties@degenspot.org",
    "decred/dcrlnd": "security@decred.org",
  };
  return maintainerMap[repository] || null;
}
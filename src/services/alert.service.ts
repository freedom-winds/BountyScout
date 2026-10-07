import type { Config } from '../types/index.js';
import { formatBountyAlert, formatBountyAlertTitle } from '../utils/formatters.js';
import type { BountyOpportunityDetail } from '../types/index.js';

export class AlertService {
  constructor(private config: Config) {}

  async createBountyAlert(opportunities: BountyOpportunityDetail[]): Promise<void> {
    const title = formatBountyAlertTitle(opportunities.length);
    const body = formatBountyAlert(opportunities);

    // TODO: Implement alert creation logic
    console.log(`Creating bounty alert: ${title}`);
    console.log(body);
  }
}

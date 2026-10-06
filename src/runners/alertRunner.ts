import { performBountyScan } from "../services/scanService.js";
import { formatBountyAlerts } from "../formatters/alertFormatter.js";
import type { Config } from "../config/types.js";

export async function runAlertJob(config: Config): Promise<string> {
  const alerts = await performBountyScan(config);
  return formatBountyAlerts(alerts);
}

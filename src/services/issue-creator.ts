import { Issue } from '../types/github';
import { logger } from '../utils/logger';

/**
 * Verifica se o conteúdo da issue deve ser criado.
 * Corrige o problema de abrir issues para relatórios de varredura (Bounty Alerts),
 * que são informativos e não representam bugs ou features.
 */
export function shouldCreateIssue(issueContent: string, issueTitle: string): boolean {
  // Padrões que indicam que a issue é apenas um relatório de varredura/alerta
  const scanReportPatterns = [
    /Bounty Alert/i,
    /Active Bounty Scan Results/i,
    /Scan Time:/i,
    /New Opportunityies found/i, // Nota: Mantendo o typo original para match exato se necessário, mas melhor usar regex flexível
    /Opportunities found/i
  ];

  const titleLower = issueTitle.toLowerCase();
  const contentLower = issueContent.toLowerCase();

  // Se o título ou conteúdo indicar que é um relatório de varredura, não criamos a issue
  // ou a marcamos como apenas um log (dependendo da implementação, aqui retornamos false para não abrir issue)
  const isScanReport = scanReportPatterns.some(pattern => 
    pattern.test(issueTitle) || pattern.test(issueContent)
  );

  if (isScanReport) {
    logger.info(`Skipping issue creation for scan report: ${issueTitle}`);
    return false;
  }

  return true;
}

export async function createIssue(repo: string, title: string, body: string, labels: string[]): Promise<void> {
  if (!shouldCreateIssue(body, title)) {
    return;
  }

  // Lógica existente de criação de issue...
  // await github.issues.create({ owner, repo, title, body, labels });
}

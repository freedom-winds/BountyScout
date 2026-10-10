import re
from datetime import datetime
from typing import List, Dict

class BountyAlertProcessor:
    def __init__(self, db_connection):
        self.db = db_connection

    def parse_scan_results(self, raw_text: str) -> List[Dict]:
        """
        Analisa o texto bruto do scan para extrair detalhes das bounties.
        """
        opportunities = []
        # Regex para capturar o padrão: [Título](URL) \n - Repository: [Repo](URL) ...
        pattern = re.compile(
            r'\d+\.\s+\[(?P<title>.*?)\]\((?P<issue_url>.*?)\)\n'
            r'- \*\*Repository:\*\* \[(?P<repo_name>.*?)\]\((?P<repo_url>.*?)\)\n'
            r'- \*\*Comments:\*\* (?P<comments>\d+)\n'
            r'- \*\*Last Updated:\*\* (?P<last_updated>.*)',
            re.MULTILINE
        )

        for match in pattern.finditer(raw_text):
            data = match.groupdict()
            opportunities.append({
                'title': data['title'],
                'issue_url': data['issue_url'],
                'repository': data['repo_name'],
                'repository_url': data['repo_url'],
                'comments': int(data['comments']),
                'last_updated': data['last_updated']
            })
        return opportunities

    async def process_new_opportunities(self, raw_report: str):
        """
        Processa o relatório, identifica novas oportunidades e evita duplicatas.
        """
        opportunities = self.parse_scan_results(raw_report)
        new_found = []

        for opp in opportunities:
            # Verifica se a issue já foi processada anteriormente no banco de dados
            exists = await self.db.check_issue_exists(opp['issue_url'])
            
            if not exists:
                await self.db.save_opportunity(opp)
                new_found.append(opp)
                print(f"🚀 New Bounty Found: {opp['title']} in {opp['repository']}")
            else:
                print(f"ℹ️ Skipping existing bounty: {opp['issue_url']}")

        return new_found

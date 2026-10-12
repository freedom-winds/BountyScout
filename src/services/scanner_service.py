from src.parsers.bounty_report_parser import BountyReportParser
import logging

class ScannerService:
    def __init__(self, db_client):
        self.parser = BountyReportParser()
        self.db = db_client
        self.logger = logging.getLogger(__name__)

    async def process_scan_report(self, report_content: str):
        """
        Processa o conteúdo de uma issue de scan e salva as novas oportunidades.
        """
        self.logger.info("Iniciando processamento de relatório de scan.")
        
        opportunities = self.parser.parse(report_content)
        
        if not opportunities:
            self.logger.warning("Nenhuma oportunidade encontrada no relatório.")
            return 0

        new_count = 0
        for opp in opportunities:
            # Verifica se a oportunidade já existe para evitar duplicatas
            exists = await self.db.check_exists(opp['issue_url'])
            if not exists:
                await self.db.save_opportunity(opp)
                new_count += 1
        
        self.logger.info(f"Processamento concluído. {new_count} novas oportunidades salvas.")
        return new_count

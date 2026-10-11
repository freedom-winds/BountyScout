import json
from datetime import datetime

def process_bounty_scan(scan_data):
    """
    Processa os resultados do scan e atualiza o registro de bounties.
    """
    processed_count = 0
    for bounty in scan_data.get('bounties', []):
        # Lógica de persistência para os novos itens detectados
        # Garantindo que o timestamp de atualização seja respeitado
        bounty['processed_at'] = datetime.utcnow().isoformat()
        save_to_db(bounty)
        processed_count += 1
    
    return {"status": "success", "count": processed_count}

def save_to_db(bounty):
    # Simulação de persistência no banco de dados
    pass

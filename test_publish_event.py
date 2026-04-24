"""
Script para simular um evento de campanha publicado no Redis.
Use para testar o chatbot localmente sem precisar do sistema de doações.

Uso:
    python test_publish_event.py
"""

import json
import redis

r = redis.from_url("redis://localhost:6379", decode_responses=True)

event = {
    "campaign_id": "camp_teste_001",
    "campaign_name": "Campanha Inverno 2026",
    "items_needed": "cobertores, agasalhos e meias",
    "donors": ["5551991045680"]
}

channel = "campanhas_doacao"
r.publish(channel, json.dumps(event))

print(f"✅ Evento publicado no canal '{channel}':")
print(json.dumps(event, indent=2, ensure_ascii=False))

import asyncio
import json
import logging
import redis.asyncio as redis
from config import settings

logger = logging.getLogger(__name__)


class RedisConsumer:
    """
    Escuta eventos de campanhas publicados no Redis e
    dispara mensagens WhatsApp para os doadores.

    Formato esperado do evento Redis:
    {
        "campaign_id": "camp_001",
        "campaign_name": "Campanha Inverno 2025",
        "items_needed": "cobertores, agasalhos e meias",
        "donors": ["5551999998888", "5551777776666"]  # Opção A: números já no evento
        # OU deixar vazio [] para buscar via DonorService (Opção B)
    }
    """

    def __init__(self, whatsapp_service, donor_service):
        self.whatsapp = whatsapp_service
        self.donor_service = donor_service
        self.redis_client = None

    async def start(self):
        logger.info(f"📡 Conectando ao Redis: {settings.REDIS_URL}")
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe(settings.REDIS_CHANNEL)

        logger.info(f"✅ Aguardando eventos no canal: '{settings.REDIS_CHANNEL}'")

        async for message in pubsub.listen():
            if message["type"] == "message":
                await self._handle_event(message["data"])

    async def _handle_event(self, raw_data: str):
        try:
            event = json.loads(raw_data)
            logger.info(f"📥 Evento recebido: campaign_id={event.get('campaign_id')}")

            # Busca a lista de doadores
            donors = await self._resolve_donors(event)

            if not donors:
                logger.warning("⚠️  Nenhum doador encontrado para esta campanha.")
                return

            logger.info(f"📨 Enviando para {len(donors)} doador(es)...")

            # Dispara mensagem para cada doador
            for donor in donors:
                await self.whatsapp.send_campaign_message(
                    phone_number=donor["phone"],
                    donor_name=donor.get("name", "Doador"),
                    campaign_name=event.get("campaign_name", "Nova Campanha"),
                    items_needed=event.get("items_needed", "insumos diversos"),
                )
                # Pequeno delay para não sobrecarregar a API
                await asyncio.sleep(0.5)

            logger.info(f"✅ Campanha {event.get('campaign_id')} enviada com sucesso.")

        except json.JSONDecodeError:
            logger.error(f"❌ Evento inválido (não é JSON): {raw_data}")
        except Exception as e:
            logger.error(f"❌ Erro ao processar evento: {e}", exc_info=True)

    async def _resolve_donors(self, event: dict) -> list:
        """
        Resolve a lista de doadores a partir do evento.

        Opção A: O evento já vem com os números dos doadores.
        Opção B: O chatbot consulta o sistema externo via API.
        """

        # --- OPÇÃO A: números já vêm no evento Redis ---
        if event.get("donors"):
            return [
                {"phone": phone, "name": "Doador"}
                for phone in event["donors"]
            ]

        # --- OPÇÃO B: busca no sistema externo de doações ---
        # Descomente quando tiver a API disponível:
        # return await self.donor_service.get_all_active_donors()

        return []

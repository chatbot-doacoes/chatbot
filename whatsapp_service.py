import logging
from twilio.rest import Client
from config import settings
import json

logger = logging.getLogger(__name__)


class WhatsAppService:
    """
    Serviço responsável por enviar mensagens WhatsApp via Twilio.
    Usa Content Templates para mensagens iniciadas pelo chatbot.
    """

    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.from_number = f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}"

    async def send_campaign_message(
        self,
        phone_number: str,
        donor_name: str,
        campaign_name: str,
        items_needed: str,
    ):
        """
        Envia a mensagem de campanha para um doador usando o Content Template.

        O template deve ter as variáveis na ordem:
          {{1}} = nome do doador
          {{2}} = nome da campanha
          {{3}} = insumos necessários
        """
        to_number = f"whatsapp:+{phone_number.lstrip('+')}"

        try:
            message = self.client.messages.create(
                to=to_number,
                from_=self.from_number,
                content_sid=settings.TWILIO_CONTENT_SID,
                content_variables=json.dumps({
                    "1": donor_name,
                    "2": campaign_name,
                    "3": items_needed,
                })
            )
            logger.info(f"✅ Mensagem enviada para {phone_number} | SID: {message.sid}")
            return message.sid

        except Exception as e:
            logger.error(f"❌ Falha ao enviar para {phone_number}: {e}")
            raise

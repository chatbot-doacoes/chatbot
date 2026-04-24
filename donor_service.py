import logging
import httpx
from config import settings

logger = logging.getLogger(__name__)


class DonorService:
    """
    Serviço para buscar doadores do sistema externo de doações.

    OPÇÃO B: use esta classe quando o sistema de doações tiver uma API.
    Por enquanto retorna dados mockados para testes.
    """

    async def get_all_active_donors(self) -> list:
        """
        Busca todos os doadores ativos.

        Quando a API estiver disponível, troque o mock pela chamada HTTP abaixo.
        """

        # --- MOCK para testes ---
        # Substitua por get_from_api() quando tiver a URL da API
        return self._get_mock_donors()

        # --- PRODUÇÃO: descomente quando tiver a API ---
        # return await self._get_from_api()

    async def _get_from_api(self) -> list:
        """Busca doadores da API do sistema externo."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.DONORS_API_URL}/donors",
                headers={"Authorization": f"Bearer {settings.DONORS_API_TOKEN}"},
                params={"active": True},
            )
            response.raise_for_status()
            data = response.json()

            # Adapte conforme o formato da resposta da API
            return [
                {
                    "phone": donor["phone"],       # ex: "5551999998888"
                    "name": donor.get("name", "Doador"),
                }
                for donor in data["donors"]
            ]

    def _get_mock_donors(self) -> list:
        """Doadores fictícios para testes no sandbox."""
        return [
            {"phone": "5551999998888", "name": "Maria Silva"},
            {"phone": "5551888887777", "name": "João Santos"},
        ]

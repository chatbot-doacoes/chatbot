# Chatbot de Arrecadação de Doações — WhatsApp

Chatbot que escuta eventos de campanhas via Redis e envia mensagens WhatsApp
para doadores cadastrados usando Twilio + WhatsApp Business API.

## Como rodar o chatbot do zero (passo a passo para novos usuários)

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
   cd NOME_DO_REPOSITORIO
   ```

2. **Crie e ative um ambiente virtual Python:**

   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**

   ```bash
   cp env.example .env
   # Edite o .env com as credenciais do Twilio e Redis
   ```

5. **Suba o Redis localmente (se necessário):**

   ```bash
   docker run -d -p 6379:6379 redis:alpine
   ```

6. **Rode o chatbot:**

   ```bash
   python main.py
   ```

7. **Simule um evento de campanha (opcional, para testes):**
   ```bash
   python test_publish_event.py
   ```

Pronto! O chatbot estará funcionando e pronto para receber eventos de campanhas.

## Estrutura

```
whatsapp-chatbot/
├── main.py               # Ponto de entrada
├── redis_consumer.py     # Escuta eventos do Redis
├── whatsapp_service.py   # Envia mensagens via Twilio
├── donor_service.py      # Busca doadores (mock ou API externa)
├── config.py             # Configurações via variáveis de ambiente
├── requirements.txt
├── .env.example          # Modelo do arquivo de configuração
└── test_publish_event.py # Simula evento Redis para testes
```

## Setup

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env com suas credenciais do Twilio
```

Onde encontrar cada valor no painel do Twilio:

- `TWILIO_ACCOUNT_SID` e `TWILIO_AUTH_TOKEN`: https://console.twilio.com (página inicial)
- `TWILIO_WHATSAPP_NUMBER`: Messaging > Senders (sandbox: +14155238886)
- `TWILIO_CONTENT_SID`: Messaging > Content Template Builder > clique no template criado

### 3. Subir o Redis localmente

```bash
docker run -d -p 6379:6379 redis:alpine
```

### 4. Rodar o chatbot

```bash
python main.py
```

### 5. Simular um evento de campanha (para testes)

Em outro terminal:

```bash
python test_publish_event.py
```

## Fluxo de dados

```
Sistema de Doações
       │
       │ publica JSON no Redis
       ▼
    Redis Pub/Sub (canal: campanhas_doacao)
       │
       │ RedisConsumer escuta
       ▼
  redis_consumer.py
       │
       ├── resolve lista de doadores
       │     ├── Opção A: donors[] já vem no evento
       │     └── Opção B: donor_service.get_all_active_donors()
       │
       ▼
  whatsapp_service.py
       │
       └── Twilio API → WhatsApp → Doador
```

## Formato do evento Redis esperado

```json
{
  "campaign_id": "camp_001",
  "campaign_name": "Campanha Inverno 2025",
  "items_needed": "cobertores, agasalhos e meias",
  "donors": ["5551999998888", "5551777776666"]
}
```

## Transição Sandbox → Produção

| Etapa           | Sandbox                     | Produção                      |
| --------------- | --------------------------- | ----------------------------- |
| Número de envio | +14155238886 (fixo Twilio)  | Seu número aprovado pela Meta |
| Template        | Não precisa aprovação       | Precisa aprovação da Meta     |
| Destinatários   | Só quem "joinnou" o sandbox | Qualquer número               |
| Custo           | Gratuito                    | Por conversa (Meta)           |

Para produzir, basta:

1. Registrar seu número como WhatsApp Business Sender no Twilio
2. Submeter o template para aprovação (`Save and Submit for WhatsApp Approval`)
3. Atualizar `TWILIO_WHATSAPP_NUMBER` no `.env`

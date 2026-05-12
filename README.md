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
   O projeto utiliza o `Pipfile`. Você pode instalar usando o pipenv:
   ```bash
   pip install pipenv
   pipenv install
   ```
   
4. **Suba o servidor localmente:**
   ```bash
   pipenv run api
   ```

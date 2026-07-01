# Bac Bo Signal Bot

Bot automatizado para monitoramento e envio de sinais do jogo Bac Bo na ElephantBet.

## Funcionalidades

- ✅ Login automático na ElephantBet
- ✅ Coleta de resultados do Bac Bo
- ✅ Análise de tendências (B/P/T)
- ✅ Envio de sinais para Telegram
- ✅ Agendamento a cada 2 minutos
- ✅ Sistema de logs completo
- ✅ Tratamento de erros robusto

## Tecnologias

- Python 3.11
- Selenium
- Telegram API
- Render (hospedagem)

## Configuração

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure as credenciais em `src/config.py`
4. Execute: `python src/main.py`

## Deploy no Render

1. Conecte o repositório ao Render
2. Selecione "Background Worker"
3. Configure `worker: python src/main.py`
4. Adicione variáveis de ambiente (opcional)

## Manutenção

- Logs disponíveis no console e Render
- Screenshots de erro sal

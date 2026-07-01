import logging
import requests
from src.config import Config

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.token = Config.TELEGRAM_TOKEN
        self.chat_id = Config.CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"
    
    def send_message(self, message: str) -> bool:
        """Envia mensagem para o Telegram de forma síncrona"""
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=Config.TIMEOUT_SECONDS
            )
            
            if response.status_code == 200:
                logger.info("Mensagem enviada com sucesso")
                return True
            else:
                logger.error(f"Erro Telegram: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return False
    
    def send_status(self, status: str):
        """Envia mensagem de status do bot"""
        return self.send_message(f"🤖 *Status do Bot Bac Bo*\n\n{status}")

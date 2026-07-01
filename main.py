import logging
import sys
from src.scheduler import BacBoScheduler
from src.config import Config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Ponto de entrada principal do bot"""
    try:
        logger.info("🤖 Iniciando Bac Bo Signal Bot")
        logger.info(f"📱 Canal: {Config.CHAT_ID}")
        logger.info(f"⏱️ Intervalo: {Config.CHECK_INTERVAL_MINUTES} minutos")
        
        scheduler = BacBoScheduler()
        scheduler.start()
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

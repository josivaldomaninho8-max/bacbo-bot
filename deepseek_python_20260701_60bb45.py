import logging
import schedule
import time
from src.telegram_bot import TelegramBot
from src.scraper import ElephantBetScraper
from src.analyzer import BacBoAnalyzer
from src.config import Config

logger = logging.getLogger(__name__)

class BacBoScheduler:
    def __init__(self):
        self.bot = TelegramBot()
        self.scraper = ElephantBetScraper()
        self.analyzer = BacBoAnalyzer()
        self.is_running = False
    
    def execute_check(self):
        """Executa uma verificação de sinais"""
        logger.info("🔍 Iniciando verificação de sinais...")
        
        try:
            # Tentar login
            if not self.scraper.is_logged_in:
                if not self.scraper.login():
                    self.bot.send_status("⚠️ Falha no login. Tentando novamente...")
                    return
            
            # Coletar resultados
            results = self.scraper.get_bacbo_results()
            if not results:
                logger.warning("Nenhum resultado coletado")
                self.bot.send_message("⚠️ Nenhum resultado disponível no momento")
                return
            
            # Analisar
            analysis = self.analyzer.analyze(results)
            
            # Enviar resultado
            message = self.analyzer.format_message(analysis)
            self.bot.send_message(message)
            
            logger.info("✅ Sinal enviado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro na execução: {e}")
            self.bot.send_message(f"❌ Erro: {str(e)[:200]}")
    
    def start(self):
        """Inicia o scheduler"""
        logger.info("🚀 Iniciando Bot de Sinais Bac Bo...")
        
        # Enviar mensagem de inicialização
        self.bot.send_status(
            "✅ *Bot Iniciado!*\n\n"
            f"🔄 Verificando a cada {Config.CHECK_INTERVAL_MINUTES} minutos\n"
            f"📊 Monitorando: Bac Bo\n"
            f"🤖 Status: Ativo"
        )
        
        # Executar primeira verificação
        self.execute_check()
        
        # Agendar verificações
        schedule.every(Config.CHECK_INTERVAL_MINUTES).minutes.do(self.execute_check)
        
        self.is_running = True
        
        # Loop principal
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
    
    def stop(self):
        """Para o scheduler"""
        self.is_running = False
        self.scraper.close()
        logger.info("🛑 Bot parado")
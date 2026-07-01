import os

class Config:
    # Telegram
    TELEGRAM_TOKEN = "8819802652:AAGs9akn3f51BY8LRvUVpp8sxT7GAmBslm4"
    CHAT_ID = "@Luckevan_bot"
    
    # ElephantBet
    USERNAME = "925959236"
    PASSWORD = "Senhas.50"
    BASE_URL = "https://elephantbet.co.ao"
    LOGIN_URL = f"{BASE_URL}/login"
    BACBO_URL = f"{BASE_URL}/pt/casino/game-view/420012128/bac-bo"
    
    # Configurações do bot
    CHECK_INTERVAL_MINUTES = 2
    MAX_RETRIES = 3
    TIMEOUT_SECONDS = 30
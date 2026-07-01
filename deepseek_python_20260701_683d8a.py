import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.config import Config

logger = logging.getLogger(__name__)

class ElephantBetScraper:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
    
    def _init_driver(self):
        """Inicializa o WebDriver com opções otimizadas"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920x1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    def login(self) -> bool:
        """Realiza login no site ElephantBet"""
        try:
            logger.info("Iniciando processo de login...")
            self.driver = self._init_driver()
            
            # Acessar página de login
            self.driver.get(Config.LOGIN_URL)
            time.sleep(5)
            
            # Aguardar e preencher campos
            wait = WebDriverWait(self.driver, 20)
            
            # Campo username
            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.clear()
            username_field.send_keys(Config.USERNAME)
            
            # Campo password
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(Config.PASSWORD)
            
            # Submeter formulário
            try:
                submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                submit_btn.click()
            except:
                password_field.send_keys(Keys.ENTER)
            
            time.sleep(8)
            
            # Verificar login
            if "login" not in self.driver.current_url.lower():
                self.is_logged_in = True
                logger.info("Login realizado com sucesso!")
                return True
            else:
                logger.error("Falha no login - ainda na página de login")
                return False
                
        except Exception as e:
            logger.error(f"Erro no login: {e}")
            if self.driver:
                self.driver.save_screenshot("login_error.png")
            return False
    
    def get_bacbo_results(self) -> list:
        """Coleta os resultados do Bac Bo"""
        if not self.is_logged_in or not self.driver:
            logger.error("Não está logado ou driver não inicializado")
            return []
        
        try:
            logger.info("Acessando página do Bac Bo...")
            self.driver.get(Config.BACBO_URL)
            time.sleep(10)
            
            # Scroll para carregar conteúdo
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
            time.sleep(3)
            
            resultados = []
            
            # Seletores para encontrar resultados
            selectors = [
                ".history-result-circle",
                ".result-circle",
                ".history-item .result",
                "[class*='history'] [class*='circle']",
                ".game-result",
                ".history-list .item"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for elem in elements[:20]:
                            text = elem.text.strip().upper()
                            if text in ["B", "P", "T"]:
                                resultados.append(text)
                            elif "BANCO" in text:
                                resultados.append("B")
                            elif "JOGADOR" in text or "PLAYER" in text:
                                resultados.append("P")
                            elif "EMPATE" in text or "TIE" in text:
                                resultados.append("T")
                        if resultados:
                            logger.info(f"Encontrados {len(resultados)} resultados")
                            break
                except:
                    continue
            
            # Fallback: buscar no HTML
            if not resultados:
                import re
                patterns = [r'[BPT](?=\s|$)', r'BANCO|JOGADOR|EMPATE']
                html = self.driver.page_source
                for pattern in patterns:
                    matches = re.findall(pattern, html)
                    for match in matches[:20]:
                        if match in ["B", "P", "T"]:
                            resultados.append(match)
                        elif "BANCO" in match:
                            resultados.append("B")
                        elif "JOGADOR" in match:
                            resultados.append("P")
                        elif "EMPATE" in match:
                            resultados.append("T")
                    if resultados:
                        break
            
            logger.info(f"Resultados coletados: {resultados[:10]}")
            return resultados
            
        except Exception as e:
            logger.error(f"Erro ao coletar resultados: {e}")
            if self.driver:
                self.driver.save_screenshot("bacbo_error.png")
            return []
    
    def close(self):
        """Fecha o WebDriver"""
        if self.driver:
            self.driver.quit()
            self.is_logged_in = False
            logger.info("Driver fechado")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
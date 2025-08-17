from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class DriverManager:
    """Manages WebDriver initialization and cleanup"""
    
    def __init__(self):
        self.driver = None
    
    def setup_driver(self, headless=False):
        """Initialize Chrome driver with options"""
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        
        if headless:
            options.add_argument("--headless")
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(30)
        return self.driver
    
    def quit_driver(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
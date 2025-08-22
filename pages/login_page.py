from selenium.webdriver.common.by import By
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_page import BasePage

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """Login Page Object with specific methods"""
    
    # Page locators
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login")
    SIGNUP_LINK = (By.LINK_TEXT, "Sign up")
    ERROR_MESSAGE = (By.CLASS_NAME, "error")
    
    # Alternative selectors for different sites
    ALT_USERNAME_FIELDS = [
        (By.NAME, "username"),
        (By.NAME, "email"),
        (By.ID, "user"),
        (By.CSS_SELECTOR, "input[type='text']"),
        (By.CSS_SELECTOR, "input[type='email']")
    ]
    
    ALT_PASSWORD_FIELDS = [
        (By.NAME, "password"),
        (By.ID, "pass"),
        (By.CSS_SELECTOR, "input[type='password']")
    ]
    
    ALT_LOGIN_BUTTONS = [
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(text(), 'Login')]"),
        (By.XPATH, "//button[contains(text(), 'Sign in')]"),
        (By.CSS_SELECTOR, ".login-btn"),
        (By.CSS_SELECTOR, ".signin-btn")
    ]
    
    def __init__(self, driver):
        super().__init__(driver)
        self.page_name = "Login Page"
    
    def login(self, username, password):
        """Perform login action with fallback selectors"""
        logger.info(f"Attempting login with username: {username}")
        
        # Try to find username field
        username_element = self._find_field_with_fallbacks(self.ALT_USERNAME_FIELDS, "username")
        if not username_element:
            logger.error("Could not find username field")
            return False
        
        # Try to find password field
        password_element = self._find_field_with_fallbacks(self.ALT_PASSWORD_FIELDS, "password")
        if not password_element:
            logger.error("Could not find password field")
            return False
        
        # Try to find login button
        login_button = self._find_field_with_fallbacks(self.ALT_LOGIN_BUTTONS, "login button")
        if not login_button:
            logger.error("Could not find login button")
            return False
        
        try:
            # Perform login sequence
            username_element.clear()
            username_element.send_keys(username)
            
            password_element.clear()
            password_element.send_keys(password)
            
            login_button.click()
            
            logger.info("Login action completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Login action failed: {str(e)}")
            return False
    
    def _find_field_with_fallbacks(self, selectors, field_name):
        """Try multiple selectors to find a field"""
        for selector in selectors:
            try:
                element = self.driver.find_element(*selector)
                if element.is_displayed() and element.is_enabled():
                    logger.debug(f"Found {field_name} using selector: {selector}")
                    return element
            except:
                continue
        
        logger.warning(f"Could not find {field_name} with any selector")
        return None
    
    def click_signup(self):
        """Click signup link with fallback selectors"""
        signup_selectors = [
            (By.LINK_TEXT, "Sign up"),
            (By.LINK_TEXT, "Register"),
            (By.PARTIAL_LINK_TEXT, "Sign up"),
            (By.PARTIAL_LINK_TEXT, "Register"),
            (By.CSS_SELECTOR, ".signup-link"),
            (By.CSS_SELECTOR, ".register-link")
        ]
        
        signup_element = self._find_field_with_fallbacks(signup_selectors, "signup link")
        if signup_element:
            try:
                signup_element.click()
                return True
            except Exception as e:
                logger.error(f"Failed to click signup link: {e}")
        
        return False
    
    def get_error_message(self):
        """Get error message if present"""
        error_selectors = [
            (By.CLASS_NAME, "error"),
            (By.CLASS_NAME, "alert-error"),
            (By.CSS_SELECTOR, ".error-message"),
            (By.CSS_SELECTOR, ".alert-danger"),
            (By.XPATH, "//*[contains(@class, 'error')]")
        ]
        
        for selector in error_selectors:
            try:
                error_element = self.find_element(selector, timeout=3)
                if error_element.is_displayed():
                    return error_element.text
            except:
                continue
        
        return None
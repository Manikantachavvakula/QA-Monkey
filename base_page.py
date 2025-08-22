from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)

class BasePage:
    """Base Page Object Model class with common functionality"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)  # Reduced from 10 for speed
        
    def find_element(self, locator, timeout=5):  # Reduced from 10
        """Find single element with explicit wait"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise NoSuchElementException(f"Element {locator} not found within {timeout} seconds")
    
    def find_elements(self, locator, timeout=5):  # Reduced from 10
        """Find multiple elements with explicit wait"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            logger.warning(f"No elements found: {locator}")
            return []
    
    def click_element(self, locator, element_name="element"):
        """Click element with error handling and logging"""
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()
            logger.info(f"Successfully clicked {element_name} - {locator}")
            return True
        except Exception as e:
            logger.error(f"Failed to click {element_name} - {locator}: {str(e)}")
            return False
    
    def enter_text(self, locator, text, element_name="input field"):
        """Enter text with error handling and logging"""
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
            logger.info(f"Successfully entered text in {element_name} - {locator}")
            return True
        except Exception as e:
            logger.error(f"Failed to enter text in {element_name} - {locator}: {str(e)}")
            return False
    
    def get_clickable_elements(self):
        """Get all clickable elements on the page"""
        clickable_selectors = [
            (By.TAG_NAME, "button"),
            (By.TAG_NAME, "a"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.CSS_SELECTOR, "input[type='button']"),
            (By.CSS_SELECTOR, "[onclick]"),
            (By.CSS_SELECTOR, ".btn"),
            (By.CSS_SELECTOR, "[role='button']")
        ]
        
        elements = []
        seen_elements = set()
        
        for locator in clickable_selectors:
            try:
                found_elements = self.driver.find_elements(*locator)
                for element in found_elements:
                    if element.is_displayed() and element.is_enabled():
                        element_id = (element.location['x'], element.location['y'], element.tag_name)
                        if element_id not in seen_elements:
                            seen_elements.add(element_id)
                            elements.append(element)
            except Exception as e:
                logger.warning(f"Error finding elements with locator {locator}: {e}")
                continue
        
        return elements
    
    def get_input_elements(self):
        """Get all input elements on the page"""
        input_selectors = [
            (By.CSS_SELECTOR, "input[type='text']"),
            (By.CSS_SELECTOR, "input[type='email']"),
            (By.CSS_SELECTOR, "input[type='search']"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.TAG_NAME, "textarea"),
            (By.CSS_SELECTOR, "input:not([type])")
        ]
        
        elements = []
        seen_elements = set()
        
        for locator in input_selectors:
            try:
                found_elements = self.driver.find_elements(*locator)
                for element in found_elements:
                    if element.is_displayed() and element.is_enabled():
                        element_id = (element.location['x'], element.location['y'], element.tag_name)
                        if element_id not in seen_elements:
                            seen_elements.add(element_id)
                            elements.append(element)
            except Exception as e:
                logger.warning(f"Error finding input elements with locator {locator}: {e}")
                continue
        
        return elements
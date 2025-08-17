from selenium.webdriver.common.by import By

class ElementLocator:
    """Handles finding elements on web pages"""
    
    def __init__(self, driver):
        self.driver = driver
    
    def get_clickable_elements(self):
        """Find all clickable elements"""
        selectors = [
            "button", "a", "input[type='submit']", "input[type='button']",
            "[onclick]", ".btn", "[role='button']"
        ]
        
        elements = []
        for selector in selectors:
            try:
                found = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for el in found:
                    if el.is_displayed() and el.is_enabled():
                        elements.append(el)
            except:
                continue
        return elements
    
    def get_input_elements(self):
        """Find all input fields"""
        selectors = [
            "input[type='text']", "input[type='email']", "input[type='search']",
            "input[type='password']", "textarea", "input:not([type])"
        ]
        
        elements = []
        for selector in selectors:
            try:
                found = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for el in found:
                    if el.is_displayed() and el.is_enabled():
                        elements.append(el)
            except:
                continue
        return elements
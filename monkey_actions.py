import random
import string
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class MonkeyActions:
    """Performs random actions on web pages"""
    
    def __init__(self, driver, element_locator):
        self.driver = driver
        self.locator = element_locator
    
    def random_string(self, length=8):
        """Generate random string for inputs"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def get_random_text(self):
        """Get random text for different input types"""
        options = [
            self.random_string(),
            f"test@example.com",
            f"Test User {random.randint(1, 1000)}",
            f"{random.randint(1, 9999)}",
            "QA Monkey Test"
        ]
        return random.choice(options)
    
    def random_click(self):
        """Perform random click"""
        elements = self.locator.get_clickable_elements()
        if elements:
            try:
                element = random.choice(elements)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.2)
                element.click()
                return True
            except:
                return False
        return False
    
    def random_scroll(self):
        """Perform random scroll"""
        scroll_options = [
            f"window.scrollBy(0, {random.randint(200, 800)})",     # Down
            f"window.scrollBy(0, -{random.randint(200, 800)})",    # Up
            "window.scrollTo(0, 0)",                               # Top
            "window.scrollTo(0, document.body.scrollHeight)"       # Bottom
        ]
        
        try:
            script = random.choice(scroll_options)
            self.driver.execute_script(script)
            return True
        except:
            return False
    
    def random_input(self):
        """Fill random text in input fields"""
        elements = self.locator.get_input_elements()
        if elements:
            try:
                element = random.choice(elements)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.2)
                element.clear()
                element.send_keys(self.get_random_text())
                return True
            except:
                return False
        return False
    
    def random_hover(self):
        """Perform random hover action"""
        elements = self.locator.get_clickable_elements()
        if elements:
            try:
                element = random.choice(elements)
                if element.is_displayed():
                    ActionChains(self.driver).move_to_element(element).perform()
                    return True
            except:
                return False
        return False
    
    def random_key_press(self):
        """Send random key presses"""
        keys_to_try = [Keys.TAB, Keys.ENTER, Keys.ESCAPE, Keys.SPACE, Keys.PAGE_DOWN]
        
        try:
            key = random.choice(keys_to_try)
            self.driver.find_element("tag name", "body").send_keys(key)
            return True
        except:
            return False
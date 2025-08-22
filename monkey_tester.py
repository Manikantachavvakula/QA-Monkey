import random
import time
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import logging

from base_page import BasePage
from pages.login_page import LoginPage
from pages.search_page import SearchPage

logger = logging.getLogger(__name__)

class EnhancedMonkeyTester:
    """Enhanced Monkey Tester using Page Object Model"""
    
    def __init__(self, driver, enhanced_logger, screenshot_manager):
        self.driver = driver
        self.logger = enhanced_logger
        self.screenshot_manager = screenshot_manager
        self.current_page = None
        self.action_weights = {
            'click': 0.35,
            'input': 0.25,
            'scroll': 0.20,
            'hover': 0.15,
            'keypress': 0.05
        }
    
    def initialize_page_object(self, url):
        """Initialize appropriate page object based on URL"""
        try:
            if 'login' in url.lower() or 'signin' in url.lower():
                self.current_page = LoginPage(self.driver)
                logger.info("Initialized LoginPage object")
            elif 'google' in url.lower() or 'search' in url.lower():
                self.current_page = SearchPage(self.driver)
                logger.info("Initialized SearchPage object")
            else:
                self.current_page = BasePage(self.driver)
                logger.info("Initialized BasePage object")
                
            return True
        except Exception as e:
            logger.error(f"Failed to initialize page object: {e}")
            return False
    
    def perform_page_specific_actions(self, url):
        """Perform page-specific actions using POM"""
        if not self.current_page:
            return False
        
        page_actions_performed = False
        
        try:
            # Login page specific actions
            if isinstance(self.current_page, LoginPage):
                if random.choice([True, False]):  # 50% chance
                    result = self.current_page.login("test_user", "test_password")
                    self.logger.log_page_action("LoginPage", "login", result)
                    page_actions_performed = True
                    
                if random.choice([True, False]):  # 50% chance
                    result = self.current_page.click_signup()
                    self.logger.log_page_action("LoginPage", "click_signup", result)
                    page_actions_performed = True
            
            # Search page specific actions
            elif isinstance(self.current_page, SearchPage):
                search_queries = ["selenium testing", "automation", "python", "QA testing", "web scraping"]
                query = random.choice(search_queries)
                result = self.current_page.search(query)
                self.logger.log_page_action("SearchPage", f"search({query})", result)
                page_actions_performed = True
                
                # Wait and check results
                if result:
                    time.sleep(2)
                    count = self.current_page.get_search_results_count()
                    logger.info(f"Search returned {count} results")
            
        except Exception as e:
            logger.error(f"Page-specific action failed: {e}")
            if self.screenshot_manager:
                self.screenshot_manager.capture_error_screenshot("page_action", str(e), url)
        
        return page_actions_performed
    
    def perform_random_monkey_action(self, url):
        """Perform random monkey testing action"""
        action_type = random.choices(
            list(self.action_weights.keys()),
            weights=list(self.action_weights.values())
        )[0]
        
        success = False
        error_msg = None
        screenshot_path = None
        element_info = "unknown"
        
        try:
            if action_type == 'click':
                success, element_info = self._random_click()
            elif action_type == 'input':
                success, element_info = self._random_input()
            elif action_type == 'scroll':
                success, element_info = self._random_scroll()
            elif action_type == 'hover':
                success, element_info = self._random_hover()
            elif action_type == 'keypress':
                success, element_info = self._random_keypress()
            
            # Capture screenshot for successful actions (occasionally)
            if success and random.random() < 0.1:  # 10% chance
                screenshot_path = self.screenshot_manager.capture_action_screenshot(action_type, url)
                
        except Exception as e:
            success = False
            error_msg = str(e)
            screenshot_path = self.screenshot_manager.capture_error_screenshot(action_type, error_msg, url)
            logger.error(f"Action {action_type} failed: {error_msg}")
        
        # Log the action
        self.logger.log_action(action_type, element_info, success, error_msg, screenshot_path)
        
        return success
    
    def _random_click(self):
        """Perform random click action"""
        if not self.current_page:
            return False, "No page object"
        
        elements = self.current_page.get_clickable_elements()
        if not elements:
            return False, "No clickable elements found"
        
        element = random.choice(elements)
        element_info = self._get_element_info(element)
        
        try:
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.2)
            
            # Try normal click first
            try:
                element.click()
                return True, element_info
            except ElementClickInterceptedException:
                # Fallback to JavaScript click
                self.driver.execute_script("arguments[0].click();", element)
                return True, f"{element_info} (JS click)"
                
        except Exception as e:
            return False, f"{element_info} - Error: {str(e)}"
    
    def _random_input(self):
        """Perform random input action"""
        if not self.current_page:
            return False, "No page object"
        
        elements = self.current_page.get_input_elements()
        if not elements:
            return False, "No input elements found"
        
        element = random.choice(elements)
        element_info = self._get_element_info(element)
        
        try:
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.2)
            
            # Generate appropriate test data
            test_data = self._generate_test_data(element)
            
            element.clear()
            element.send_keys(test_data)
            
            return True, f"{element_info} = '{test_data}'"
            
        except Exception as e:
            return False, f"{element_info} - Error: {str(e)}"
    
    def _random_scroll(self):
        """Perform random scroll action"""
        scroll_actions = [
            ("window.scrollBy(0, 300)", "Scroll down"),
            ("window.scrollBy(0, -300)", "Scroll up"),
            ("window.scrollTo(0, 0)", "Scroll to top"),
            ("window.scrollTo(0, document.body.scrollHeight)", "Scroll to bottom"),
            ("window.scrollBy(200, 0)", "Scroll right"),
            ("window.scrollBy(-200, 0)", "Scroll left")
        ]
        
        script, description = random.choice(scroll_actions)
        
        try:
            self.driver.execute_script(script)
            return True, description
        except Exception as e:
            return False, f"{description} - Error: {str(e)}"
    
    def _random_hover(self):
        """Perform random hover action"""
        if not self.current_page:
            return False, "No page object"
        
        elements = self.current_page.get_clickable_elements()
        if not elements:
            return False, "No hoverable elements found"
        
        element = random.choice(elements)
        element_info = self._get_element_info(element)
        
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            return True, f"Hover on {element_info}"
        except Exception as e:
            return False, f"Hover on {element_info} - Error: {str(e)}"
    
    def _random_keypress(self):
        """Perform random key press action"""
        keys_to_try = [
            (Keys.TAB, "Tab"),
            (Keys.ENTER, "Enter"),
            (Keys.ESCAPE, "Escape"),
            (Keys.SPACE, "Space"),
            (Keys.PAGE_DOWN, "Page Down"),
            (Keys.PAGE_UP, "Page Up"),
            (Keys.HOME, "Home"),
            (Keys.END, "End")
        ]
        
        key, description = random.choice(keys_to_try)
        
        try:
            body = self.driver.find_element("tag name", "body")
            body.send_keys(key)
            return True, f"Key press: {description}"
        except Exception as e:
            return False, f"Key press: {description} - Error: {str(e)}"
    
    def _get_element_info(self, element):
        """Get descriptive information about an element"""
        try:
            tag = element.tag_name
            element_id = element.get_attribute('id')
            element_class = element.get_attribute('class')
            element_text = element.text[:20] if element.text else ""
            
            info_parts = [f"<{tag}"]
            if element_id:
                info_parts.append(f" id='{element_id}'")
            if element_class:
                info_parts.append(f" class='{element_class[:20]}'")
            info_parts.append(">")
            
            if element_text:
                info_parts.append(f" '{element_text}'")
            
            return "".join(info_parts)
        except:
            return f"<{element.tag_name}>"
    
    def _generate_test_data(self, element):
        """Generate appropriate test data based on input type"""
        try:
            input_type = element.get_attribute('type')
            placeholder = element.get_attribute('placeholder')
            name = element.get_attribute('name')
            
            # Email inputs
            if input_type == 'email' or 'email' in (name or '').lower():
                return f"test{random.randint(1, 999)}@example.com"
            
            # Password inputs
            elif input_type == 'password':
                return f"TestPass{random.randint(100, 999)}"
            
            # Search inputs
            elif input_type == 'search' or 'search' in (name or '').lower():
                search_terms = ["automation", "testing", "selenium", "python", "QA"]
                return random.choice(search_terms)
            
            # Number inputs
            elif input_type == 'number':
                return str(random.randint(1, 100))
            
            # URL inputs
            elif input_type == 'url':
                return "https://example.com"
            
            # Default text
            else:
                text_options = [
                    f"Test User {random.randint(1, 999)}",
                    f"Sample Text {random.randint(1, 999)}",
                    "QA Automation Test",
                    f"TestData{random.randint(1000, 9999)}",
                    "Monkey Testing Input"
                ]
                return random.choice(text_options)
                
        except:
            return f"TestInput{random.randint(1, 999)}"
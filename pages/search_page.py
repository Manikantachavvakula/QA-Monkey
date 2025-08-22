from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_page import BasePage

logger = logging.getLogger(__name__)

class SearchPage(BasePage):
    """Search Page Object for Google-like search functionality"""
    
    # Primary search selectors
    SEARCH_BOX = (By.NAME, "q")
    SEARCH_BUTTON = (By.NAME, "btnK")
    RESULTS_CONTAINER = (By.ID, "search")
    
    # Alternative search selectors for different sites
    ALT_SEARCH_BOXES = [
        (By.NAME, "q"),
        (By.NAME, "query"),
        (By.NAME, "search"),
        (By.ID, "search"),
        (By.ID, "query"),
        (By.CSS_SELECTOR, "input[type='search']"),
        (By.CSS_SELECTOR, ".search-input"),
        (By.CSS_SELECTOR, ".search-box"),
        (By.XPATH, "//input[@placeholder*='search' or @placeholder*='Search']")
    ]
    
    ALT_SEARCH_BUTTONS = [
        (By.NAME, "btnK"),
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(text(), 'Search')]"),
        (By.CSS_SELECTOR, ".search-btn"),
        (By.CSS_SELECTOR, ".search-button")
    ]
    
    def __init__(self, driver):
        super().__init__(driver)
        self.page_name = "Search Page"
    
    def search(self, query):
        """Perform search action with fallback selectors"""
        logger.info(f"Searching for: {query}")
        
        # Find search box
        search_box = self._find_search_element(self.ALT_SEARCH_BOXES, "search box")
        if not search_box:
            logger.error("Could not find search box")
            return False
        
        try:
            # Clear and enter search term
            search_box.clear()
            search_box.send_keys(query)
            
            # Try pressing Enter first (most reliable)
            search_box.send_keys(Keys.RETURN)
            logger.info(f"Search submitted for query: {query}")
            return True
            
        except Exception as e:
            logger.error(f"Search failed for query {query}: {str(e)}")
            
            # Fallback: try clicking search button
            try:
                search_button = self._find_search_element(self.ALT_SEARCH_BUTTONS, "search button")
                if search_button:
                    search_button.click()
                    logger.info(f"Search submitted via button for query: {query}")
                    return True
            except Exception as btn_error:
                logger.error(f"Search button fallback also failed: {btn_error}")
        
        return False
    
    def _find_search_element(self, selectors, element_name):
        """Find search element with fallback selectors"""
        for selector in selectors:
            try:
                element = self.driver.find_element(*selector)
                if element.is_displayed() and element.is_enabled():
                    logger.debug(f"Found {element_name} using selector: {selector}")
                    return element
            except:
                continue
        
        logger.warning(f"Could not find {element_name} with any selector")
        return None
    
    def get_search_results_count(self):
        """Get number of search results with multiple strategies"""
        result_selectors = [
            (By.CSS_SELECTOR, ".g"),           # Google results
            (By.CSS_SELECTOR, ".result"),      # Generic results
            (By.CSS_SELECTOR, ".search-result"), # Alternative
            (By.XPATH, "//div[contains(@class, 'result')]")
        ]
        
        for selector in result_selectors:
            try:
                results = self.find_elements(selector, timeout=5)
                if results:
                    count = len(results)
                    logger.info(f"Found {count} search results using {selector}")
                    return count
            except:
                continue
        
        logger.warning("Could not count search results")
        return 0
    
    def click_first_result(self):
        """Click the first search result"""
        result_selectors = [
            (By.CSS_SELECTOR, ".g a"),
            (By.CSS_SELECTOR, ".result a"),
            (By.CSS_SELECTOR, ".search-result a")
        ]
        
        for selector in result_selectors:
            try:
                first_result = self.driver.find_element(*selector)
                if first_result.is_displayed():
                    first_result.click()
                    logger.info("Clicked first search result")
                    return True
            except:
                continue
        
        logger.warning("Could not click first search result")
        return False
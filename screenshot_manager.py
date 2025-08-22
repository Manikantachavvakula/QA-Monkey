import os
from datetime import datetime
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class EnhancedScreenshotManager:
    """Enhanced screenshot management with error capture"""
    
    def __init__(self, driver, session_id):
        self.driver = driver
        self.session_id = session_id
        self.setup_directories()
        self.screenshot_count = 0
    
    def setup_directories(self):
        """Setup screenshot directories"""
        self.base_dir = f"screenshots/{self.session_id}"
        self.error_dir = f"{self.base_dir}/errors"
        self.action_dir = f"{self.base_dir}/actions"
        
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.error_dir, exist_ok=True)
        os.makedirs(self.action_dir, exist_ok=True)
    
    def capture_error_screenshot(self, action_type, error_msg, url=""):
        """Capture screenshot when error occurs"""
        try:
            timestamp = datetime.now().strftime("%H%M%S_%f")[:-3]  # Include milliseconds
            url_name = self._get_url_name(url)
            error_clean = self._clean_filename(error_msg)
            
            filename = f"{timestamp}_ERROR_{action_type}_{error_clean}_{url_name}.png"
            filepath = os.path.join(self.error_dir, filename)
            
            if self.driver.save_screenshot(filepath):
                self.screenshot_count += 1
                logger.info(f"Error screenshot saved: {filepath}")
                return filepath
            else:
                logger.error("Failed to save error screenshot")
                return None
                
        except Exception as e:
            logger.error(f"Error capturing screenshot: {e}")
            return None
    
    def capture_action_screenshot(self, action_type, url=""):
        """Capture screenshot for successful action"""
        try:
            timestamp = datetime.now().strftime("%H%M%S_%f")[:-3]
            url_name = self._get_url_name(url)
            
            filename = f"{timestamp}_{action_type}_{url_name}.png"
            filepath = os.path.join(self.action_dir, filename)
            
            if self.driver.save_screenshot(filepath):
                self.screenshot_count += 1
                logger.debug(f"Action screenshot saved: {filepath}")
                return filepath
            else:
                logger.warning("Failed to save action screenshot")
                return None
                
        except Exception as e:
            logger.warning(f"Error capturing action screenshot: {e}")
            return None
    
    def _get_url_name(self, url):
        """Extract clean domain name from URL"""
        try:
            if url:
                domain = urlparse(url).netloc.replace('www.', '')
                return self._clean_filename(domain)
            return "unknown"
        except:
            return "unknown"
    
    def _clean_filename(self, text):
        """Clean text for use in filename"""
        if not text:
            return "unknown"
        
        # Replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            text = text.replace(char, '_')
        
        # Limit length and remove extra spaces
        return text.strip()[:30]
    
    def get_screenshot_stats(self):
        """Get screenshot statistics"""
        return {
            'total_screenshots': self.screenshot_count,
            'base_directory': self.base_dir,
            'error_directory': self.error_dir,
            'action_directory': self.action_dir
        }
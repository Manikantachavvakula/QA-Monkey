import os
from datetime import datetime
from urllib.parse import urlparse

class ScreenshotHandler:
    """Handles screenshot capture and storage"""
    
    def __init__(self, driver, session_id):
        self.driver = driver
        self.session_id = session_id
        self.screenshot_dir = f"screenshots/{session_id}"
        self.setup_directories()
        self.screenshot_count = 0
    
    def setup_directories(self):
        """Create screenshot directories"""
        os.makedirs(self.screenshot_dir, exist_ok=True)
        os.makedirs(f"{self.screenshot_dir}/errors", exist_ok=True)
        os.makedirs(f"{self.screenshot_dir}/actions", exist_ok=True)
    
    def clean_filename(self, text):
        """Clean text for filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            text = text.replace(char, '_')
        return text[:30]  # Limit length
    
    def get_url_name(self, url):
        """Get clean domain name from URL"""
        try:
            domain = urlparse(url).netloc.replace('www.', '')
            return self.clean_filename(domain)
        except:
            return "unknown"
    
    def capture_screenshot(self, url, action_type, is_error=False, error_msg=""):
        """Capture screenshot"""
        try:
            timestamp = datetime.now().strftime("%H%M%S")
            url_name = self.get_url_name(url)
            
            if is_error:
                error_clean = self.clean_filename(error_msg)
                filename = f"{timestamp}_error_{action_type}_{error_clean}_{url_name}.png"
                filepath = f"{self.screenshot_dir}/errors/{filename}"
            else:
                filename = f"{timestamp}_{action_type}_{url_name}.png"
                filepath = f"{self.screenshot_dir}/actions/{filename}"
            
            # Take screenshot
            success = self.driver.save_screenshot(filepath)
            
            if success:
                self.screenshot_count += 1
                return filepath
            else:
                return None
                
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return None
    
    def get_stats(self):
        """Get screenshot statistics"""
        return {
            "total_screenshots": self.screenshot_count,
            "directory": self.screenshot_dir
        }
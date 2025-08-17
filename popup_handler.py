from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class PopupHandler:
    """Handles various types of popups and modals"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 2)  # Short wait for popups
    
    def close_popups(self):
        """Try to close any visible popups"""
        popup_closed = False
        
        # Try to close Google sign-in dialogs first (high priority)
        popup_closed |= self._close_google_signin()
        
        # Try to close other login/signup modals
        popup_closed |= self._close_login_modals()
        
        # Try to close cookie/consent banners
        popup_closed |= self._close_cookie_banners()
        
        # Try to close modal dialogs
        popup_closed |= self._close_modal_dialogs()
        
        # Try to close notification prompts
        popup_closed |= self._close_notification_prompts()
        
        # Handle JavaScript alerts
        popup_closed |= self._handle_js_alerts()
        
        # Try pressing Escape key as last resort
        popup_closed |= self._press_escape()
        
        return popup_closed
    
    def _close_cookie_banners(self):
        """Close cookie consent banners"""
        cookie_selectors = [
            # Common cookie banner buttons
            "[data-testid*='accept']",
            "[data-testid*='cookie']",
            "button[id*='accept']",
            "button[id*='cookie']",
            "button[class*='accept']",
            "button[class*='cookie']",
            ".cookie-banner button",
            ".consent-banner button",
            "#cookieChoiceDismiss",
            ".cookie-accept",
            ".accept-cookies",
            "[aria-label*='Accept']",
            "[aria-label*='Close']"
        ]
        
        for selector in cookie_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed() and element.is_enabled():
                    element.click()
                    print("🍪 Closed cookie banner")
                    return True
            except:
                continue
        
        return False
    
    def _close_modal_dialogs(self):
        """Close modal dialogs"""
        modal_selectors = [
            # Common modal close buttons
            ".modal .close",
            ".modal button[aria-label='Close']",
            ".dialog .close",
            ".popup .close",
            "button[data-dismiss='modal']",
            ".modal-close",
            ".close-modal",
            "[role='dialog'] button",
            ".overlay .close",
            "button.btn-close",
            ".modal-header .close",
            "[aria-label*='close' i]",
            "[title*='close' i]"
        ]
        
        for selector in modal_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed() and element.is_enabled():
                    element.click()
                    print("📱 Closed modal dialog")
                    return True
            except:
                continue
        
        return False
    
    def _close_notification_prompts(self):
        """Close browser notification prompts"""
        notification_selectors = [
            # Notification permission prompts
            "button[data-testid*='notification']",
            ".notification-bar button",
            ".notification-prompt button"
        ]
        
        for selector in notification_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed() and element.is_enabled():
                    element.click()
                    print("🔔 Dismissed notification prompt")
                    return True
            except:
                continue
        
        return False
    
    def _handle_js_alerts(self):
        """Handle JavaScript alerts, confirms, and prompts"""
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text[:50]
            alert.dismiss()  # Click Cancel/No
            print(f"⚠️ Dismissed JS alert: {alert_text}")
            return True
        except:
            return False
    
    def _close_google_signin(self):
        """Specifically handle Google sign-in popups"""
        try:
            # Try to find "Stay signed out" button using JavaScript
            script = """
            var buttons = document.querySelectorAll('button, div[role="button"]');
            for (var i = 0; i < buttons.length; i++) {
                var text = buttons[i].textContent || buttons[i].innerText;
                if (text && text.includes('Stay signed out')) {
                    buttons[i].click();
                    return true;
                }
            }
            return false;
            """
            result = self.driver.execute_script(script)
            if result:
                print("🔒 Closed Google sign-in dialog")
                return True
        except:
            pass
        
        # Try other Google-specific selectors
        google_selectors = [
            "[aria-label*='Close']",
            "[title*='Close']", 
            "button[data-dismiss]",
            "[data-value='cancel']"
        ]
        
        for selector in google_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed() and element.is_enabled():
                    element.click()
                    print("🔒 Closed Google dialog")
                    return True
            except:
                continue
        
        return False
    
    def _close_login_modals(self):
        """Close login/signup modals"""
        try:
            # Try to find common dismissal buttons
            script = """
            var buttons = document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                var text = buttons[i].textContent || buttons[i].innerText;
                if (text && (text.includes('Skip') || text.includes('Not now') || text.includes('Maybe later') || text.includes('No thanks'))) {
                    buttons[i].click();
                    return true;
                }
            }
            return false;
            """
            result = self.driver.execute_script(script)
            if result:
                print("🚪 Closed login modal")
                return True
        except:
            pass
        
        return False
    
    def _press_escape(self):
        """Press Escape key to close modals"""
        try:
            from selenium.webdriver.common.keys import Keys
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)
            print("⌨️ Pressed Escape to close modal")
            return True
        except:
            return False
    
    def force_close_all_modals(self):
        """Aggressive approach to close all modals"""
        try:
            # Method 1: Click "Stay signed out" specifically for Google
            stay_signed_out_script = """
            var buttons = document.querySelectorAll('button, div[role="button"]');
            for (var i = 0; i < buttons.length; i++) {
                var text = buttons[i].textContent || buttons[i].innerText;
                if (text && (text.includes('Stay signed out') || text.includes('No thanks') || text.includes('Cancel'))) {
                    buttons[i].click();
                    return 'Clicked: ' + text;
                }
            }
            return 'No button found';
            """
            result = self.driver.execute_script(stay_signed_out_script)
            if result and 'Clicked:' in str(result):
                print(f"🎯 Force closed: {result}")
                return True
            
            # Method 2: Press Escape multiple times
            from selenium.webdriver.common.keys import Keys
            body = self.driver.find_element(By.TAG_NAME, "body")
            for _ in range(3):
                body.send_keys(Keys.ESCAPE)
            
            # Method 3: Remove modal elements entirely
            remove_modals_script = """
            var modals = document.querySelectorAll('[role="dialog"], .modal, .popup, [class*="modal"], [id*="modal"]');
            var count = modals.length;
            for (var i = 0; i < modals.length; i++) {
                modals[i].remove();
            }
            
            var overlays = document.querySelectorAll('[class*="backdrop"], [class*="overlay"], [style*="position: fixed"]');
            for (var i = 0; i < overlays.length; i++) {
                if (overlays[i].style.zIndex > 100) {
                    overlays[i].remove();
                }
            }
            
            return count + ' modals removed';
            """
            result = self.driver.execute_script(remove_modals_script)
            print(f"🗑️ Force removed modals: {result}")
            
            return True
            
        except Exception as e:
            print(f"⚠️ Force close failed: {e}")
            return False
    
    def dismiss_overlays(self):
        """Dismiss any overlay elements that might block interactions"""
        overlay_selectors = [
            ".overlay",
            ".backdrop",
            ".modal-backdrop",
            ".popup-overlay"
        ]
        
        for selector in overlay_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        self.driver.execute_script("arguments[0].click();", element)
                        print("🎭 Dismissed overlay")
                        return True
            except:
                continue
        
        return False
    
    def handle_gdpr_banners(self):
        """Specifically handle GDPR/privacy banners"""
        gdpr_selectors = [
            "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
            "#onetrust-accept-btn-handler",
            ".ot-sdk-row button",
            "[data-gdpr-accept]",
            "button[id*='gdpr']",
            "button[class*='gdpr']",
            ".gdpr-banner button",
            ".privacy-banner button"
        ]
        
        for selector in gdpr_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed() and element.is_enabled():
                    element.click()
                    print("🛡️ Accepted GDPR banner")
                    return True
            except:
                continue
        
        return False
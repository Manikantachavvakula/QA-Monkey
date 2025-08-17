import random
import time
from datetime import datetime
from driver_manager import DriverManager
from element_locator import ElementLocator
from monkey_actions import MonkeyActions
from test_config import TestConfig
from simple_logger import SimpleLogger
from screenshot_handler import ScreenshotHandler
from popup_handler import PopupHandler

class MonkeyTester:
    """Main monkey testing orchestrator"""
    
    def __init__(self):
        self.driver_manager = DriverManager()
        self.driver = None
        self.locator = None
        self.actions = None
        self.start_time = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.logger = SimpleLogger(self.session_id)
        self.screenshot_handler = None
        self.popup_handler = None
        
        self.stats = {
            "total_actions": 0,
            "successful_clicks": 0,
            "successful_scrolls": 0,
            "successful_inputs": 0,
            "successful_hovers": 0,
            "errors": 0,
            "urls_tested": 0,
            "urls_failed": 0
        }
    
    def setup(self, headless=False):
        """Initialize all components"""
        print("🔧 Setting up QA-Monkey...")
        
        self.driver = self.driver_manager.setup_driver(headless)
        self.locator = ElementLocator(self.driver)
        self.actions = MonkeyActions(self.driver, self.locator)
        self.start_time = datetime.now()
        
        print("✅ Setup complete!")
    
    def run_single_test(self, url, iterations=None):
        """Run monkey test on a single URL"""
        if iterations is None:
            iterations = TestConfig.DEFAULT_ITERATIONS
            
        print(f"\n{'='*60}")
        print(f"🌐 Testing: {url}")
        print(f"🎯 Actions: {iterations}")
        print(f"{'='*60}")
        
        try:
            print("📡 Loading page...")
            self.driver.get(url)
            time.sleep(TestConfig.PAGE_LOAD_WAIT)
            
            # Handle popups immediately after page load
            try:
                if self.popup_handler:
                    popup_closed = self.popup_handler.close_popups()
                    if popup_closed:
                        time.sleep(1)  # Wait a bit after closing popups
                    
                    # Try GDPR banners specifically
                    self.popup_handler.handle_gdpr_banners()
                    
                    # If popups are still there, force close them
                    time.sleep(2)  # Wait to see if popups appear
                    self.popup_handler.force_close_all_modals()
                
            except Exception as e:
                print(f"⚠️ Popup handling failed: {e}")
            
            page_title = self.driver.title[:50] + "..." if len(self.driver.title) > 50 else self.driver.title
            print(f"📄 Page loaded: {page_title}")
            
            self.stats["urls_tested"] += 1
            
            for i in range(iterations):
                # Periodically check for and close popups during testing
                if i % 2 == 0:  # Every 2nd action (more frequent)
                    try:
                        if self.popup_handler:
                            self.popup_handler.close_popups()
                            # If regular popup closing fails, force close
                            if i == 0:  # First action, be more aggressive
                                self.popup_handler.force_close_all_modals()
                    except:
                        pass
                
                self.perform_random_action(i + 1, iterations, url)
                delay = random.uniform(TestConfig.MIN_DELAY, TestConfig.MAX_DELAY)
                time.sleep(delay)
                
            print(f"✅ Completed testing {url}")
                
        except Exception as e:
            print(f"❌ Error with {url}: {str(e)[:60]}...")
            self.stats["errors"] += 1
            self.stats["urls_failed"] += 1
    
    def perform_random_action(self, current, total, url):
        """Execute a single random action"""
        actions = ["click", "scroll", "input", "hover"]
        weights = [
            TestConfig.ACTION_WEIGHTS["click"],
            TestConfig.ACTION_WEIGHTS["scroll"],
            TestConfig.ACTION_WEIGHTS["input"],
            TestConfig.ACTION_WEIGHTS["hover"]
        ]
        
        action = random.choices(actions, weights=weights)[0]
        self.stats["total_actions"] += 1
        
        success = False
        error_msg = None
        screenshot_path = None
        
        try:
            if action == "click":
                success = self.actions.random_click()
                if success:
                    self.stats["successful_clicks"] += 1
                    if self.screenshot_handler:
                        screenshot_path = self.screenshot_handler.capture_screenshot(url, action)
                    
            elif action == "scroll":
                success = self.actions.random_scroll()
                if success:
                    self.stats["successful_scrolls"] += 1
                    
            elif action == "input":
                success = self.actions.random_input()
                if success:
                    self.stats["successful_inputs"] += 1
                    if self.screenshot_handler:
                        screenshot_path = self.screenshot_handler.capture_screenshot(url, action)
                    
            elif action == "hover":
                success = self.actions.random_hover()
                if success:
                    self.stats["successful_hovers"] += 1
            
            # Log the result
            status = "PASS" if success else "FAIL"
            self.logger.log_test_result(url, action, status, error_msg, screenshot_path)
            
            status_icon = "✅" if success else "❌"
            progress = f"[{current:2d}/{total}]"
            action_text = f"{action.upper():<8}"
            
            print(f"{progress} {action_text} {status_icon}")
            
        except Exception as e:
            error_msg = str(e)
            if self.screenshot_handler:
                screenshot_path = self.screenshot_handler.capture_screenshot(url, action, True, error_msg)
            
            # Log error
            self.logger.log_test_result(url, action, "ERROR", error_msg, screenshot_path)
            self.logger.log_error(url, action, error_msg, screenshot_path)
            
            print(f"[{current:2d}/{total}] {action.upper():<8} ❌ Error: {error_msg[:40]}...")
            self.stats["errors"] += 1
    
    def run_category_test(self, category="comprehensive"):
        """Run tests based on predefined categories"""
        config = TestConfig.get_test_config(category)
        print(f"🐒 Starting QA-Monkey - {category.upper()} Test")
        print(f"📊 URLs: {len(config['urls'])}")
        print(f"🎯 Actions per URL: {config['iterations']}")
        
        self.run_multiple_tests(config['urls'], config['iterations'])
    
    def run_multiple_tests(self, urls=None, iterations_per_url=None):
        """Run tests on multiple URLs"""
        if urls is None:
            urls = TestConfig.URLS
        if iterations_per_url is None:
            iterations_per_url = TestConfig.DEFAULT_ITERATIONS
        
        print(f"\n🐒 QA-Monkey Testing Started!")
        print(f"⏰ Start time: {self.start_time.strftime('%H:%M:%S')}")
        print(f"🌐 URLs to test: {len(urls)}")
        print(f"🎯 Actions per URL: {iterations_per_url}")
        
        try:
            for i, url in enumerate(urls, 1):
                print(f"\n🔄 Progress: {i}/{len(urls)} URLs")
                try:
                    self.run_single_test(url, iterations_per_url)
                except KeyboardInterrupt:
                    print("\n⚠️  Test interrupted by user")
                    break
                except Exception as e:
                    print(f"⚠️  Skipping {url} due to error: {str(e)[:50]}...")
                    self.stats["urls_failed"] += 1
                    continue
        finally:
            self.print_final_stats()
    
    def print_final_stats(self):
        """Print comprehensive test statistics"""
        end_time = datetime.now()
        duration = end_time - self.start_time if self.start_time else None
        
        print(f"\n{'='*60}")
        print("🐒 QA-MONKEY TEST RESULTS")
        print(f"{'='*60}")
        
        if duration:
            print(f"⏱️  Duration:           {str(duration).split('.')[0]}")
        
        print(f"🌐 URLs tested:        {self.stats['urls_tested']}")
        print(f"❌ URLs failed:        {self.stats['urls_failed']}")
        print(f"🎯 Total actions:      {self.stats['total_actions']}")
        print(f"\n📊 ACTION BREAKDOWN:")
        print(f"   Clicks:             {self.stats['successful_clicks']}")
        print(f"   Scrolls:            {self.stats['successful_scrolls']}")
        print(f"   Inputs:             {self.stats['successful_inputs']}")
        print(f"   Hovers:             {self.stats['successful_hovers']}")
        print(f"   Errors:             {self.stats['errors']}")
        
        # Calculate success rate
        total_successful = (
            self.stats['successful_clicks'] + 
            self.stats['successful_scrolls'] + 
            self.stats['successful_inputs'] +
            self.stats['successful_hovers']
        )
        
        if self.stats['total_actions'] > 0:
            success_rate = (total_successful / self.stats['total_actions']) * 100
            print(f"\n📈 Success rate:       {success_rate:.1f}%")
            
            if success_rate >= 80:
                print("🎉 Excellent success rate!")
            elif success_rate >= 60:
                print("👍 Good success rate!")
            else:
                print("⚠️  Consider checking website compatibility")
        
        print(f"{'='*60}")
    
    def cleanup(self):
        """Clean up resources and generate reports"""
        print("🧹 Cleaning up...")
        
        # Save all logs and generate reports
        try:
            files = self.logger.save_logs_to_file()
            html_report = self.logger.generate_html_report()
            
            print(f"Reports generated:")
            print(f"   JSON: {files['json_file']}")
            print(f"   CSV: {files['csv_file']}")
            print(f"   HTML: {html_report}")
            if files.get('error_file'):
                print(f"   Errors: {files['error_file']}")
            
            if self.screenshot_handler:
                screenshot_stats = self.screenshot_handler.get_stats()
                print(f"Screenshots: {screenshot_stats['total_screenshots']} saved to {screenshot_stats['directory']}")
            
            # Print summary
            print(self.logger.get_summary())
            
        except Exception as e:
            print(f"Warning: Could not save reports: {e}")
        
        self.driver_manager.quit_driver()
        print("✅ Cleanup complete!")
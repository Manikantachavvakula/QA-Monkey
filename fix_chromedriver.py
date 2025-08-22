#!/usr/bin/env python3
"""
ChromeDriver Fix Script - Solves version mismatch issues
"""

import os
import shutil
import subprocess
import sys

def clear_webdriver_cache():
    """Clear WebDriver Manager cache"""
    try:
        # Windows path
        cache_path = os.path.expanduser("~/.wdm")
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
            print("✅ Cleared WebDriver Manager cache")
        else:
            print("ℹ️ No WebDriver cache found")
    except Exception as e:
        print(f"⚠️ Could not clear cache: {e}")

def update_webdriver_manager():
    """Update webdriver-manager to latest version"""
    try:
        print("🔄 Updating webdriver-manager...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "webdriver-manager"])
        print("✅ Updated webdriver-manager")
    except Exception as e:
        print(f"❌ Failed to update webdriver-manager: {e}")

def test_chromedriver():
    """Test if ChromeDriver works"""
    try:
        print("🧪 Testing ChromeDriver...")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Simple test
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ ChromeDriver test successful! Page title: {title}")
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver test failed: {e}")
        return False

def main():
    print("""
🔧 CHROMEDRIVER FIX UTILITY
==========================
This script will:
1. Clear WebDriver Manager cache
2. Update webdriver-manager
3. Test ChromeDriver functionality
""")
    
    input("Press Enter to continue...")
    
    print("\n🔄 Step 1: Clearing WebDriver cache...")
    clear_webdriver_cache()
    
    print("\n🔄 Step 2: Updating webdriver-manager...")
    update_webdriver_manager()
    
    print("\n🔄 Step 3: Testing ChromeDriver...")
    if test_chromedriver():
        print("\n🎉 SUCCESS! ChromeDriver is working correctly.")
        print("You can now run: python main_runner.py")
    else:
        print("\n❌ ChromeDriver still not working.")
        print("\n📋 MANUAL STEPS:")
        print("1. Update Chrome browser to latest version")
        print("2. Restart your computer")
        print("3. Run this script again")
        print("4. If still failing, try: python main_runner.py --headless")

if __name__ == "__main__":
    main()
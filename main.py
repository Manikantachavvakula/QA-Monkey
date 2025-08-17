#!/usr/bin/env python3
"""
QA-Monkey: Automated Random Web Testing Tool

A streamlined monkey testing tool that performs random actions on websites
to discover potential issues, crashes, or unexpected behaviors.

Usage:
    python main.py                    # Run comprehensive test
    python main.py --quick           # Quick test
    python main.py --extended        # Extended test
    python main.py --url <URL>       # Test single URL
"""

import sys
import argparse
from monkey_tester import MonkeyTester

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="QA-Monkey: Random Web Testing Tool")
    
    parser.add_argument("--quick", action="store_true",
                       help="Run quick test (3 URLs, 10 actions each)")
    
    parser.add_argument("--extended", action="store_true",
                       help="Run extended test (30 actions per URL)")
    
    parser.add_argument("--url", type=str,
                       help="Test a single specific URL")
    
    parser.add_argument("--actions", type=int, default=20,
                       help="Number of actions per URL (default: 20)")
    
    parser.add_argument("--headless", action="store_true",
                       help="Run browser in headless mode")
    
    return parser.parse_args()

def display_banner():
    """Display startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                          QA-MONKEY                           ║
║                  Automated Web Testing Tool                  ║
║                                                              ║
║  🐒 Performs random clicks, scrolls, and inputs            ║
║  🎯 Tests multiple websites automatically                   ║
║  📊 Provides detailed statistics and reporting             ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def get_custom_urls():
    """Interactive URL input for custom testing"""
    print("\n🔧 CUSTOM URL TESTING")
    print("Enter URLs to test (press Enter after each URL, empty line to finish):")
    
    urls = []
    while True:
        url = input(f"URL {len(urls) + 1}: ").strip()
        if not url:
            break
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        urls.append(url)
        print(f"✅ Added: {url}")
    
    return urls if urls else ["https://example.com"]

def run_interactive_mode():
    """Interactive mode for selecting test options"""
    print("\n🎮 INTERACTIVE MODE")
    print("Choose your testing approach:")
    print("1. Quick Test (3 URLs, 10 actions each)")
    print("2. Comprehensive Test (All URLs, 20 actions each)")
    print("3. Extended Test (All URLs, 30 actions each)")
    print("4. Custom URLs")
    print("5. Single URL")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                return "quick", None, None
            elif choice == "2":
                return "comprehensive", None, None
            elif choice == "3":
                return "extended", None, None
            elif choice == "4":
                urls = get_custom_urls()
                actions = int(input("Actions per URL (default 20): ") or "20")
                return "custom", urls, actions
            elif choice == "5":
                url = input("Enter URL: ").strip()
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                actions = int(input("Number of actions (default 20): ") or "20")
                return "single", url, actions
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Invalid input or cancelled.")
            return "comprehensive", None, None

def main():
    """Main entry point for QA-Monkey testing"""
    
    # Display banner
    display_banner()
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Initialize tester
    tester = MonkeyTester()
    
    try:
        # Setup browser
        tester.setup(headless=args.headless)
        
        # Determine test mode based on arguments
        if args.url:
            # Single URL testing
            print(f"\n🎯 SINGLE URL TEST MODE")
            tester.run_single_test(args.url, args.actions)
            
        elif args.quick:
            # Quick test mode
            print(f"\n⚡ QUICK TEST MODE")
            tester.run_category_test("quick")
            
        elif args.extended:
            # Extended test mode
            print(f"\n🚀 EXTENDED TEST MODE")
            tester.run_category_test("extended")
            
        else:
            # Default comprehensive testing
            print(f"\n📋 COMPREHENSIVE TEST MODE")
            tester.run_category_test("comprehensive")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Testing stopped by user (Ctrl+C)")
        tester.print_final_stats()
        
    except Exception as e:
        print(f"\n🚨 Fatal error occurred: {e}")
        print("📋 Please check your setup:")
        print("   1. Selenium installed: pip install selenium")
        print("   2. ChromeDriver available in PATH")
        print("   3. Chrome browser installed")
        
    finally:
        # Always cleanup
        tester.cleanup()
        print("\n🎉 QA-Monkey testing session completed!")

if __name__ == "__main__":
    # Check if running without arguments for interactive mode
    if len(sys.argv) == 1:
        try:
            mode, param1, param2 = run_interactive_mode()
            
            tester = MonkeyTester()
            tester.setup()
            
            if mode == "single":
                tester.run_single_test(param1, param2)
            elif mode == "custom":
                tester.run_multiple_tests(param1, param2)
            else:
                tester.run_category_test(mode)
                
            tester.cleanup()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        except Exception as e:
            print(f"Error: {e}")
    else:
        main()
#!/usr/bin/env python3
"""
Enhanced QA-Monkey Regression Test Runner
Supports the resume claim: "achieving 92% success in regression testing"
"""

import sys
import argparse
from regression_test_suite import RegressionTestSuite

def get_custom_websites():
    """Get custom websites from user input"""
    print("\n🌐 CUSTOM WEBSITE TESTING")
    print("=" * 50)
    
    # Ask how many websites to test
    while True:
        try:
            max_sites = int(input("How many websites do you want to test? (1-20): "))
            if 1 <= max_sites <= 20:
                break
            else:
                print("❌ Please enter a number between 1 and 20")
        except ValueError:
            print("❌ Please enter a valid number")
    
    websites = []
    
    print(f"\nEnter {max_sites} websites to test:")
    print("Example: google.com (https:// will be added automatically)")
    
    for i in range(max_sites):
        while True:
            website = input(f"Website {i + 1}/{max_sites}: ").strip()
            
            if website:
                # Add https:// if not present
                if not website.startswith(('http://', 'https://')):
                    website = 'https://' + website
                    
                websites.append(website)
                print(f"✅ Added: {website}")
                break
            else:
                print("❌ Please enter a website URL")
    
    print(f"\n📋 Will test {len(websites)} websites:")
    for i, site in enumerate(websites, 1):
        print(f"   {i}. {site}")
    
    return websites

def choose_test_mode():
    """Let user choose test mode - optimized for speed"""
    print("\n⚡ SELECT TEST MODE (All modes run in HEADLESS for speed)")
    print("=" * 60)
    print("1. Lightning (2 actions per site) - ~10 seconds per site")
    print("2. Quick (5 actions per site) - ~20 seconds per site") 
    print("3. Standard (8 actions per site) - ~30 seconds per site")
    print("4. Extended (12 actions per site) - ~45 seconds per site")
    print("5. Custom (specify number of actions)")
    
    while True:
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                return 2, "Lightning", 0.3  # actions, name, delay
            elif choice == '2':
                return 5, "Quick", 0.5
            elif choice == '3':
                return 8, "Standard", 0.7
            elif choice == '4':
                return 12, "Extended", 1.0
            elif choice == '5':
                while True:
                    try:
                        actions = int(input("Enter number of actions per website (1-25): "))
                        if 1 <= actions <= 25:
                            delay = min(1.0, actions * 0.1)  # Dynamic delay based on actions
                            return actions, f"Custom ({actions} actions)", delay
                        else:
                            print("❌ Please enter a number between 1 and 25")
                    except ValueError:
                        print("❌ Please enter a valid number")
            else:
                print("❌ Please enter 1, 2, 3, 4, or 5")
                
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Invalid input. Please try again.")

def main():
    parser = argparse.ArgumentParser(description="Enhanced QA-Monkey Regression Test Suite")
    parser.add_argument("--target-rate", type=float, default=92.0,
                      help="Target success rate percentage (default: 92.0)")
    parser.add_argument("--super-fast", action="store_true",
                      help="Super fast mode: 2 actions per site, 3 sites max")
    parser.add_argument("--quick", action="store_true",
                      help="Quick mode: 5 actions per site")
    parser.add_argument("--interactive", action="store_true",
                      help="Interactive mode to choose websites and settings")
    parser.add_argument("--visible", action="store_true",
                      help="Run with visible browser (default: headless for speed)")
    
    args = parser.parse_args()
    
    # Force headless by default for speed (opposite of original)
    headless_mode = not args.visible
    
    # Display banner
    print("""
╔══════════════════════════════════════════════════════════════╗
║              ENHANCED QA-MONKEY TEST SUITE                   ║
║         Python-Selenium with POM Design Pattern             ║
║                                                              ║
║  🎯 Target Success Rate: {:.1f}%                           ║
║  🐒 Randomized User Actions with Smart Selection            ║
║  📊 Multi-Format Reports (HTML/JSON/CSV)                   ║
║  📸 Automatic Error Screenshots                            ║
║  📝 Detailed Structured Logging                            ║
║  ⚡ SPEED OPTIMIZED - HEADLESS BY DEFAULT                  ║
║  🚀 NEW: Super Fast Mode & Website Count Selection         ║
╚══════════════════════════════════════════════════════════════╝
    """.format(args.target_rate))
    
    # Initialize test suite
    suite = RegressionTestSuite(target_success_rate=args.target_rate)
    
    # Interactive mode
    if args.interactive:
        # Get custom websites with count selection
        custom_websites = get_custom_websites()
        suite.test_urls = custom_websites
        
        # Choose test mode with speed optimization
        max_actions, mode_name, action_delay = choose_test_mode()
        suite.smart_config['max_actions_per_url'] = max_actions
        suite.smart_config['action_delay_range'] = (action_delay, action_delay + 0.2)  # Faster delays
        suite.smart_config['page_load_wait'] = 1.5  # Faster page load wait
        
        print(f"\n🚀 STARTING {mode_name.upper()} TEST")
        print(f"🎯 Target Success Rate: {args.target_rate}%")
        print(f"🌐 Testing {len(suite.test_urls)} websites")
        print(f"⚡ {max_actions} actions per website")
        print(f"👁️  Mode: {'Visible Browser' if args.visible else 'Headless (Fast)'}")
        print(f"⏱️  Estimated time: ~{len(suite.test_urls) * max_actions * action_delay / 60:.1f} minutes")
        
        input("\nPress Enter to start testing...")
    else:
        # Set default fast configuration for non-interactive mode
        suite.smart_config['page_load_wait'] = 1.5
        suite.smart_config['action_delay_range'] = (0.3, 0.5)
    
    try:
        # Setup with headless by default
        suite.setup(headless=headless_mode)
        
        # Adjust for quick test modes (if not in interactive mode)
        if args.super_fast and not args.interactive:
            suite.smart_config['max_actions_per_url'] = 2
            suite.smart_config['action_delay_range'] = (0.1, 0.3)  # Ultra fast
            suite.smart_config['page_load_wait'] = 1
            suite.test_urls = suite.test_urls[:3]  # Only 3 websites
            print("⚡ SUPER FAST MODE: 2 actions per site, 3 sites max")
        elif args.quick and not args.interactive:
            suite.smart_config['max_actions_per_url'] = 5
            suite.smart_config['action_delay_range'] = (0.2, 0.4)  # Fast
            suite.smart_config['page_load_wait'] = 1.5
            suite.test_urls = suite.test_urls[:4]  # 4 websites
            print("⚡ QUICK MODE: 5 actions per site, 4 sites max")
        
        # Run tests
        final_stats = suite.run_regression_tests()
        
        # Generate reports
        reports = suite.generate_reports()
        
        # Print final summary matching resume claim
        print(f"\n🎉 RESUME-READY SUMMARY:")
        print(f"   Framework: Python-Selenium with POM design")
        print(f"   Features: Randomized actions, detailed logging, screenshots, multi-format reports")
        print(f"   Achievement: {final_stats['success_rate']:.0f}% success in regression testing")
        print(f"   Test Evidence: {reports['html']}")
        
        # Ask if user wants to view the HTML report (only if not headless)
        if not headless_mode:
            try:
                view_report = input(f"\n📊 Open HTML report in browser? (y/n): ").strip().lower()
                if view_report in ['y', 'yes']:
                    import webbrowser
                    import os
                    report_path = os.path.abspath(reports['html'])
                    webbrowser.open(f'file://{report_path}')
                    print(f"🌐 Report opened in browser: {report_path}")
            except KeyboardInterrupt:
                pass
        else:
            # In headless mode, show where report is located
            import os
            report_path = os.path.abspath(reports['html'])
            print(f"\n📊 HTML Report saved at: {report_path}")
            print(f"📁 Open this file in your browser to view results")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test suite interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        print("\n🔧 TROUBLESHOOTING TIPS:")
        print("1. Update Chrome: https://www.google.com/chrome/")
        print("2. Update ChromeDriver: pip install --upgrade webdriver-manager")
        print("3. Clear cache: Delete ~/.wdm folder (Windows: %USERPROFILE%/.wdm)")
        print("4. Try visible mode: python main_runner.py --visible")
    finally:
        suite.cleanup()

if __name__ == "__main__":
    main()
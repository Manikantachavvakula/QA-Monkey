#!/usr/bin/env python3
"""
Example test runner showing different ways to use the framework
"""

import sys
import os
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from regression_test_suite import RegressionTestSuite

def run_login_focused_test():
    """Run test focused on login functionality - FAST"""
    print("🔐 Running Login-Focused Test (FAST)")
    
    # Create suite with login-heavy URLs
    suite = RegressionTestSuite(target_success_rate=90.0)
    suite.test_urls = [
        "https://the-internet.herokuapp.com/login",
        "https://demoqa.com/login",
        "https://httpbin.org/forms/post"
    ]
    
    # Adjust for fast login testing
    suite.smart_config['max_actions_per_url'] = 5  # Reduced from 10
    suite.smart_config['action_delay_range'] = (0.3, 0.5)  # Faster
    suite.smart_config['page_load_wait'] = 1.5  # Faster
    
    try:
        suite.setup(headless=True)  # Always headless for speed
        stats = suite.run_regression_tests()
        reports = suite.generate_reports()
        
        print(f"Login Test Results: {stats['success_rate']}% success rate")
        return stats
    finally:
        suite.cleanup()

def run_search_focused_test():
    """Run test focused on search functionality - FAST"""
    print("🔍 Running Search-Focused Test (FAST)")
    
    suite = RegressionTestSuite(target_success_rate=95.0)
    suite.test_urls = [
        "https://www.google.com",
        "https://duckduckgo.com",
        "https://github.com/search"
    ]
    
    # Fast search testing
    suite.smart_config['max_actions_per_url'] = 4  # Reduced from 8
    suite.smart_config['action_delay_range'] = (0.2, 0.4)  # Faster
    suite.smart_config['page_load_wait'] = 1.5  # Faster
    
    try:
        suite.setup(headless=True)  # Always headless for speed
        stats = suite.run_regression_tests()
        reports = suite.generate_reports()
        
        print(f"Search Test Results: {stats['success_rate']}% success rate")
        return stats
    finally:
        suite.cleanup()

def run_comprehensive_regression():
    """Run full regression suite - OPTIMIZED"""
    print("🎯 Running Comprehensive Regression Test (OPTIMIZED)")
    
    suite = RegressionTestSuite(target_success_rate=92.0)
    
    # Optimize for comprehensive but fast testing
    suite.smart_config['max_actions_per_url'] = 6  # Balanced
    suite.smart_config['action_delay_range'] = (0.4, 0.7)  # Reasonable speed
    suite.smart_config['page_load_wait'] = 2  # Balanced
    
    try:
        suite.setup(headless=True)  # Always headless for speed
        stats = suite.run_regression_tests()
        reports = suite.generate_reports()
        
        # Print detailed summary
        print(f"\n{'='*60}")
        print(f"🏆 COMPREHENSIVE TEST COMPLETED")
        print(f"{'='*60}")
        print(f"Total Actions: {stats['total_actions']}")
        print(f"Success Rate: {stats['success_rate']}%")
        print(f"Target Met: {'✅ YES' if stats['success_rate'] >= 92.0 else '❌ NO'}")
        print(f"HTML Report: {reports.get('html', 'Not generated')}")
        
        return stats
    finally:
        suite.cleanup()

def run_lightning_demo():
    """Ultra-fast demo mode - 30 seconds total"""
    print("⚡ Running Lightning Demo (30 seconds)")
    
    suite = RegressionTestSuite(target_success_rate=90.0)
    suite.test_urls = [
        "https://www.google.com",
        "https://github.com"
    ]
    
    # Ultra-fast settings
    suite.smart_config['max_actions_per_url'] = 2
    suite.smart_config['action_delay_range'] = (0.1, 0.3)
    suite.smart_config['page_load_wait'] = 1
    
    try:
        suite.setup(headless=True)
        stats = suite.run_regression_tests()
        reports = suite.generate_reports()
        
        print(f"⚡ Lightning Demo Results: {stats['success_rate']}% success rate")
        print(f"📊 Report: {reports.get('html', 'Not generated')}")
        return stats
    finally:
        suite.cleanup()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type == "login":
            run_login_focused_test()
        elif test_type == "search":
            run_search_focused_test()
        elif test_type == "comprehensive":
            run_comprehensive_regression()
        elif test_type == "lightning" or test_type == "demo":
            run_lightning_demo()
        else:
            print("Usage: python test_runner_example.py [login|search|comprehensive|lightning]")
            print("  login        - Fast login functionality testing")
            print("  search       - Fast search functionality testing") 
            print("  comprehensive - Full regression testing (optimized)")
            print("  lightning    - Ultra-fast demo (30 seconds)")
    else:
        # Default: run lightning demo for quick results
        print("🚀 Running default Lightning Demo...")
        print("For other options: python test_runner_example.py [login|search|comprehensive|lightning]")
        run_lightning_demo()
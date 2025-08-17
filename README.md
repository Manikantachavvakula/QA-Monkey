# QA-Monkey 🐒

**Comprehensive Automated Web Testing Tool with Advanced Reporting**

QA-Monkey is a professional-grade monkey testing tool that performs random actions on websites to discover potential issues, crashes, or unexpected behaviors. Built with Python and Selenium using Page Object Model (POM) architecture, it provides enterprise-level logging, error tracking, screenshot capture, and comprehensive reporting.

## 🚀 Features

- **Random Actions**: Clicks, scrolls, inputs, hovers, and key presses
- **Multiple URLs**: Test Google, GitHub, StackOverflow, and more
- **POM Architecture**: Clean, maintainable code structure
- **Comprehensive Logging**: Detailed logs with session tracking
- **Screenshot Capture**: Automatic screenshots on actions and errors
- **Test Case Management**: Pass/fail tracking with detailed reports
- **Error Handling**: Advanced error detection, categorization, and insights
- **Multiple Report Formats**: HTML, JSON, CSV reports with charts
- **Executive Summaries**: High-level reports for management
- **Flexible Configuration**: Easy to customize and extend

## 📁 Project Structure

```
qa-monkey/
├── driver_manager.py      # WebDriver setup and management
├── element_locator.py     # Element finding and selection
├── monkey_actions.py      # Random action implementations
├── test_config.py        # URLs and configuration settings
├── monkey_tester.py      # Main test orchestrator
├── logger_manager.py     # Comprehensive logging system
├── screenshot_manager.py # Screenshot capture and management
├── test_case_manager.py  # Test case tracking and reporting
├── error_handler.py      # Error detection and analysis
├── report_generator.py   # Multi-format report generation
├── main.py              # Entry point and CLI interface
├── requirements.txt     # Python dependencies
└── README.md           # This file

# Generated during testing:
├── logs/                # Session logs and error tracking
├── screenshots/         # Captured screenshots organized by session
├── test_results/        # Test case results in multiple formats
├── errors/              # Error reports and analysis
└── reports/             # Comprehensive test reports
```

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Chrome browser installed
- ChromeDriver (auto-managed by webdriver-manager)

### Step 1: Clone or Download
```bash
git clone https://github.com/your-repo/qa-monkey.git
cd qa-monkey
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python -c "from selenium import webdriver; print('✅ Selenium ready!')"
```

## 🎮 Usage

### Quick Start
```bash
# Run interactive mode (recommended for first time)
python main.py

# Run comprehensive test (all URLs, 30 actions each)
python main.py --comprehensive

# Quick test (5 URLs, 15 actions each)
python main.py --quick

# Google services only
python main.py --google

# Extended testing (50 actions per URL)
python main.py --extended

# Single URL testing
python main.py --url https://example.com --actions 25

# Custom URLs with interactive selection
python main.py --custom
```

### Advanced Usage
```bash
# Headless mode (faster, no GUI)
python main.py --headless

# Test specific category with custom actions
python main.py --google --actions 40

# Single URL with detailed analysis
python main.py --url https://github.com --actions 100
```

## 🌐 Tested Websites

### Search Engines
- **Google.com** - Search, Images, Maps, Translate
- **Bing.com** - Microsoft search engine

### Developer Platforms
- **GitHub.com** - Code repositories and collaboration
- **StackOverflow.com** - Programming Q&A platform
- **CodePen.io** - Frontend code playground
- **JSFiddle.net** - JavaScript testing environment

### Testing & Demo Sites
- **Example.com** - Simple demonstration site
- **HTTPBin.org** - HTTP testing service with forms
- **The-Internet.herokuapp.com** - Selenium practice site
- **DemoQA.com** - UI testing elements

### E-commerce Examples
- **Demo.OpenCart.com** - E-commerce demo platform
- **AutomationExercise.com** - Practice e-commerce site

### Content & Educational
- **News.YCombinator.com** - Tech news aggregator
- **W3Schools.com** - Web development tutorials

## 🎯 Test Categories

| Category | URLs | Actions/URL | Description | Use Case |
|----------|------|-------------|-------------|----------|
| `quick` | 5 | 15 | Fast testing for development | Daily CI/CD checks |
| `comprehensive` | 14 | 30 | Full test suite (default) | Weekly regression testing |
| `google_focused` | 5 | 25 | Google services testing | Specific platform testing |
| `extended` | 14 | 50 | Thorough testing | Pre-release validation |

## 🎯 Action Types

1. **Random Clicks** (35%): Buttons, links, clickable elements
2. **Random Scrolls** (25%): Up, down, left, right, top, bottom
3. **Random Inputs** (25%): Text fields, emails, search boxes
4. **Random Hovers** (10%): Mouse over elements
5. **Random Key Presses** (5%): Tab, Enter, Escape, navigation keys

## 📊 Generated Reports & Files

### 📝 Logs
- **Main Log**: `logs/qa_monkey_YYYYMMDD_HHMMSS.log`
- **Error Log**: `logs/errors/errors_YYYYMMDD_HHMMSS.log`
- **Action Log**: `logs/actions/actions_YYYYMMDD_HHMMSS.log`
- **Session Data**: `logs/sessions/session_YYYYMMDD_HHMMSS.json`

### 📸 Screenshots
- **Page Screenshots**: `screenshots/SESSION_ID/pages/`
- **Action Screenshots**: `screenshots/SESSION_ID/actions/`
- **Error Screenshots**: `screenshots/SESSION_ID/errors/`
- **HTML Report**: `screenshots/SESSION_ID/screenshot_report.html`

### 📋 Test Results
- **JSON Results**: `test_results/json/test_results_SESSION_ID.json`
- **CSV Results**: `test_results/csv/test_results_SESSION_ID.csv`
- **HTML Report**: `test_results/html/test_report_SESSION_ID.html`
- **Failed Cases**: `test_results/json/failed_cases_SESSION_ID.json`

### 🚨 Error Reports
- **Error JSON**: `errors/reports/error_report_SESSION_ID.json`
- **Error HTML**: `errors/reports/error_report_SESSION_ID.html`
- **Error CSV**: `errors/reports/errors_SESSION_ID.csv`
- **Critical Errors**: `errors/critical/critical_SESSION_ID_*.json`

### 📊 Master Reports
- **Comprehensive HTML**: `reports/html/master_report_SESSION_ID.html`
- **Executive Summary**: `reports/executive/executive_summary_SESSION_ID.html`
- **Master JSON**: `reports/json/master_report_SESSION_ID.json`

## 📈 Example Output

```
🐒 QA-MONKEY TEST RESULTS
============================================================
⏱️  Duration:           00:02:45
🌐 URLs tested:        5
❌ URLs failed:        0
🎯 Total actions:      150

📊 ACTION BREAKDOWN:
   Clicks:             45
   Scrolls:            38
   Inputs:             32
   Hovers:             15
   Key presses:        8
   Errors:             12

📈 Success rate:       92.0%
🎉 Excellent success rate!
⚡ Actions per minute:  54.5

📋 GENERATING REPORTS...
✅ Reports generated successfully!
📁 Master Report: reports/html/master_report_20241204_143022.html
📊 Test Results: test_results/html/test_report_20241204_143022.html
🚨 Error Report: errors/reports/error_report_20241204_143022.html
📸 Screenshot Report: screenshots/20241204_143022/screenshot_report.html

💡 ERROR INSIGHTS:
   • Most problematic action: click (8 errors)
   • Critical errors that need immediate attention: 0
   • Frequent error patterns detected: 2

📁 Session files saved with ID: 20241204_143022
============================================================
```

## 🔧 Configuration

### Basic Configuration (`test_config.py`)
```python
# Add your own URLs
URLS = [
    "https://your-website.com",
    "https://another-site.com"
]

# Adjust action probabilities
ACTION_WEIGHTS = {
    "click": 0.35,
    "scroll": 0.25,
    "input": 0.25,
    "hover": 0.10,
    "keypress": 0.05
}

# Timing settings
DEFAULT_ITERATIONS = 30
MIN_DELAY = 0.5
MAX_DELAY = 2.0
PAGE_LOAD_WAIT = 3
```

### Advanced Settings
```python
# Browser options
BROWSER_OPTIONS = {
    "headless": False,
    "maximize_window": True,
    "implicit_wait": 10,
    "page_load_timeout": 30
}

# Error handling
MAX_RETRIES = 3
RETRY_DELAY = 1
```

## 🛡️ Safety Features

- **Element Validation**: Checks if elements are visible and enabled
- **Error Recovery**: Continues testing even when individual actions fail
- **Timeout Protection**: Prevents hanging on slow pages
- **Graceful Cleanup**: Always closes browser properly
- **Interrupt Handling**: Safe exit with Ctrl+C
- **Smart Error Detection**: Stops testing if too many critical errors occur
- **Screenshot Evidence**: Captures what happened for debugging

## 📊 Report Features

### HTML Reports Include:
- **Interactive Charts**: Visual representation of test results
- **Clickable Screenshots**: View full-size images
- **Error Analysis**: Categorized by severity and frequency
- **Action Statistics**: Success rates by action type
- **URL Performance**: Which sites had the most issues
- **Executive Summary**: High-level overview for management

### JSON/CSV Reports Include:
- **Detailed Test Cases**: Individual action results
- **Error Records**: Complete error information
- **Session Metadata**: Configuration and timing data
- **Statistical Analysis**: Calculated metrics and insights

## 🔍 Advanced Usage

### Programmatic Usage
```python
from monkey_tester import MonkeyTester

# Initialize tester
tester = MonkeyTester()
tester.setup()

# Test specific URLs
custom_urls = ["https://example.com", "https://github.com"]
tester.run_multiple_tests(custom_urls, 20)

# Access results
test_stats = tester.test_case_manager.get_statistics()
error_summary = tester.error_handler.get_error_summary()

# Generate reports
reports = tester.report_generator.generate_all_reports()

# Cleanup
tester.cleanup()
```

### Custom Actions
```python
# In monkey_actions.py
def custom_action(self):
    """Your custom testing action"""
    try:
        # Implement your action logic
        return True
    except Exception:
        return False

# In test_config.py
ACTION_WEIGHTS = {
    "click": 0.30,
    "scroll": 0.25,
    "input": 0.25,
    "hover": 0.10,
    "custom": 0.10  # Add your custom action
}
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Run QA-Monkey Tests
  run: |
    python main.py --quick --headless
    
- name: Upload Test Reports
  uses: actions/upload-artifact@v3
  with:
    name: qa-monkey-reports
    path: |
      reports/
      logs/
      screenshots/
```

## 🐛 Troubleshooting

### Common Issues

**1. ChromeDriver not found**
```bash
# Install webdriver-manager (included in requirements.txt)
pip install webdriver-manager

# Or download manually and add to PATH
export PATH=$PATH:/path/to/chromedriver
```

**2. Chrome browser not found**
```bash
# Install Chrome browser first
# Ubuntu/Debian:
sudo apt-get install google-chrome-stable

# macOS:
brew install --cask google-chrome
```

**3. Permission errors**
```bash
# Make sure ChromeDriver is executable
chmod +x chromedriver

# Check Python permissions
python --version
which python
```

**4. Slow performance**
- Reduce `DEFAULT_ITERATIONS` in `test_config.py`
- Increase `MIN_DELAY` for slower testing
- Use `--headless` flag for faster execution
- Close other applications to free resources

**5. Memory issues**
- Use `--headless` mode
- Reduce number of URLs tested
- Clean up old screenshots and logs
- Monitor system resources

### Best Practices

✅ **DO:**
- Start with `--quick` mode to verify setup
- Use headless mode for CI/CD pipelines
- Test on staging environments, not production
- Review error logs for recurring issues
- Monitor system resources during extended tests
- Keep screenshots and logs for evidence

❌ **DON'T:**
- Run on production systems without permission
- Ignore critical errors in reports
- Run too many concurrent sessions
- Delete logs immediately after testing
- Skip configuration review for your environment

## 📊 Understanding Reports

### Success Rate Interpretation
- **90%+**: Excellent application stability
- **75-89%**: Good performance, minor issues
- **50-74%**: Moderate issues, needs attention
- **<50%**: Significant problems, review required

### Error Severity Levels
- **CRITICAL**: Browser crashes, connection failures
- **HIGH**: Element not found, timeouts
- **MEDIUM**: Element not interactable, click intercepted
- **LOW**: Minor UI issues, harmless errors

### Key Metrics to Monitor
- **Actions per minute**: Performance indicator
- **Error patterns**: Recurring issues
- **URL success rates**: Site-specific problems
- **Action type success**: Which actions fail most

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-action`)
3. Add your changes with tests
4. Update documentation
5. Submit pull request

### Development Setup
```bash
# Clone repository
git clone https://github.com/your-repo/qa-monkey.git
cd qa-monkey

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
python -m pytest tests/

# Format code
black *.py
```

## 📝 License

MIT License - Feel free to use and modify for your testing needs!

## 🔗 Related Tools

- **Selenium**: Web automation framework
- **Chaos Monkey**: Infrastructure chaos engineering
- **Artillery**: Load testing tool
- **Puppeteer**: Node.js web automation
- **WebDriver Manager**: Automatic driver management

## 📞 Support

- **Issues**: Report bugs and request features on GitHub
- **Documentation**: Check inline code comments
- **Examples**: See `examples/` directory for usage patterns
- **Community**: Join discussions in GitHub Issues

## 🎯 Roadmap

### Upcoming Features
- [ ] Mobile browser testing (Chrome Mobile, Safari)
- [ ] API endpoint testing integration
- [ ] Machine learning for smarter action selection
- [ ] Real-time dashboard for monitoring
- [ ] Integration with popular CI/CD platforms
- [ ] Performance metrics collection
- [ ] A/B testing capabilities
- [ ] Custom assertion framework

### Version History
- **v1.0.0**: Initial release with basic monkey testing
- **v2.0.0**: Added POM architecture and multiple browsers
- **v3.0.0**: Comprehensive logging and reporting system
- **v4.0.0**: Advanced error handling and screenshots
- **v5.0.0**: Executive reporting and test case management

---

**Happy Testing! 🐒🎉**

*Built with ❤️ for QA engineers who want comprehensive automated testing with professional reporting.*

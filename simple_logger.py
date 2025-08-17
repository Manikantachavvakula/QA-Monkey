import os
import json
import csv
from datetime import datetime

class SimpleLogger:
    """Simple logging and reporting manager"""
    
    def __init__(self, session_id):
        self.session_id = session_id
        self.setup_directories()
        self.test_results = []
        self.errors = []
        self.stats = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0
        }
    
    def setup_directories(self):
        """Create necessary directories"""
        dirs = ["logs", "reports", "screenshots", "errors"]
        for directory in dirs:
            os.makedirs(directory, exist_ok=True)
    
    def log_test_result(self, url, action, status, error_msg=None, screenshot_path=None):
        """Log individual test result"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "action": action,
            "status": status,  # PASS, FAIL, ERROR
            "error_message": error_msg,
            "screenshot_path": screenshot_path
        }
        
        self.test_results.append(result)
        self.stats["total_tests"] += 1
        
        if status == "PASS":
            self.stats["passed"] += 1
        elif status == "FAIL":
            self.stats["failed"] += 1
        else:
            self.stats["errors"] += 1
    
    def log_error(self, url, action, error_msg, screenshot_path=None):
        """Log error details"""
        error = {
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "action": action,
            "error": error_msg,
            "screenshot_path": screenshot_path
        }
        self.errors.append(error)
    
    def save_logs_to_file(self):
        """Save all logs to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save test results as JSON
        json_file = f"logs/test_results_{self.session_id}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "stats": self.stats,
                "results": self.test_results
            }, f, indent=2, ensure_ascii=False)
        
        # Save test results as CSV
        csv_file = f"logs/test_results_{self.session_id}.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "URL", "Action", "Status", "Error", "Screenshot"])
            for result in self.test_results:
                writer.writerow([
                    result["timestamp"],
                    result["url"],
                    result["action"],
                    result["status"],
                    result.get("error_message", ""),
                    result.get("screenshot_path", "")
                ])
        
        # Save errors
        if self.errors:
            error_file = f"errors/errors_{self.session_id}.json"
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(self.errors, f, indent=2, ensure_ascii=False)
        
        return {
            "json_file": json_file,
            "csv_file": csv_file,
            "error_file": f"errors/errors_{self.session_id}.json" if self.errors else None
        }
    
    def generate_html_report(self):
        """Generate HTML report"""
        html_file = f"reports/report_{self.session_id}.html"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>QA-Monkey Test Report - {self.session_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: #ecf0f1; padding: 15px; border-radius: 8px; text-align: center; }}
        .stat-number {{ font-size: 2em; font-weight: bold; }}
        .pass {{ color: #27ae60; }}
        .fail {{ color: #e74c3c; }}
        .error {{ color: #f39c12; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #34495e; color: white; }}
        tr:nth-child(even) {{ background: #f2f2f2; }}
        .PASS {{ background: #d5f4e6; }}
        .FAIL {{ background: #ffeaa7; }}
        .ERROR {{ background: #fab1a0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🐒 QA-Monkey Test Report</h1>
        <p>Session: {self.session_id}</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{self.stats['total_tests']}</div>
            <div>Total Tests</div>
        </div>
        <div class="stat-card pass">
            <div class="stat-number">{self.stats['passed']}</div>
            <div>Passed</div>
        </div>
        <div class="stat-card fail">
            <div class="stat-number">{self.stats['failed']}</div>
            <div>Failed</div>
        </div>
        <div class="stat-card error">
            <div class="stat-number">{self.stats['errors']}</div>
            <div>Errors</div>
        </div>
    </div>
    
    <h2>Test Results</h2>
    <table>
        <tr>
            <th>Timestamp</th>
            <th>URL</th>
            <th>Action</th>
            <th>Status</th>
            <th>Error</th>
            <th>Screenshot</th>
        </tr>
"""
        
        for result in self.test_results:
            timestamp = result["timestamp"].split("T")[1][:8]
            url_short = result["url"][:50] + "..." if len(result["url"]) > 50 else result["url"]
            error_msg = result.get("error_message", "")[:50] if result.get("error_message") else ""
            screenshot = "📸" if result.get("screenshot_path") else ""
            
            html_content += f"""
        <tr class="{result['status']}">
            <td>{timestamp}</td>
            <td>{url_short}</td>
            <td>{result['action'].upper()}</td>
            <td><strong>{result['status']}</strong></td>
            <td>{error_msg}</td>
            <td>{screenshot}</td>
        </tr>
            """
        
        html_content += """
    </table>
</body>
</html>
        """
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_file
    
    def get_summary(self):
        """Get test summary"""
        total = self.stats["total_tests"]
        if total == 0:
            return "No tests completed"
        
        success_rate = (self.stats["passed"] / total) * 100
        return f"""
TEST SUMMARY
Session: {self.session_id}
Total Tests: {total}
Passed: {self.stats['passed']}
Failed: {self.stats['failed']}
Errors: {self.stats['errors']}
Success Rate: {success_rate:.1f}%
        """
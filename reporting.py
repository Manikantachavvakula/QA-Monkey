import json
import csv
import os
from datetime import datetime
from jinja2 import Template
import logging

logger = logging.getLogger(__name__)

class EnhancedReporting:
    """Multi-format reporting system"""
    
    def __init__(self, session_id, test_results, stats, screenshot_manager=None):
        self.session_id = session_id
        self.test_results = test_results
        self.stats = stats
        self.screenshot_manager = screenshot_manager
        self.setup_directories()
    
    def setup_directories(self):
        """Setup report directories"""
        self.report_dir = f"reports/{self.session_id}"
        os.makedirs(self.report_dir, exist_ok=True)
        os.makedirs(f"{self.report_dir}/csv", exist_ok=True)
        os.makedirs(f"{self.report_dir}/json", exist_ok=True)
        os.makedirs(f"{self.report_dir}/html", exist_ok=True)
    
    def generate_csv_report(self):
        """Generate CSV report"""
        csv_file = f"{self.report_dir}/csv/test_results.csv"
        
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Timestamp', 'Action Type', 'Element Info', 'Status', 
                    'Error Message', 'Screenshot Path'
                ])
                
                for result in self.test_results:
                    writer.writerow([
                        result['timestamp'],
                        result['action_type'],
                        result['element_info'],
                        result['status'],
                        result.get('error_msg', ''),
                        result.get('screenshot_path', '')
                    ])
            
            logger.info(f"CSV report generated: {csv_file}")
            return csv_file
            
        except Exception as e:
            logger.error(f"Failed to generate CSV report: {e}")
            return None
    
    def generate_json_report(self):
        """Generate JSON report"""
        json_file = f"{self.report_dir}/json/test_results.json"
        
        try:
            report_data = {
                'session_id': self.session_id,
                'generated_at': datetime.now().isoformat(),
                'statistics': self.stats,
                'test_results': self.test_results,
                'summary': {
                    'total_tests': len(self.test_results),
                    'passed': len([r for r in self.test_results if r['result']]),
                    'failed': len([r for r in self.test_results if not r['result']]),
                    'success_rate_percent': self.stats.get('success_rate', 0)
                }
            }
            
            if self.screenshot_manager:
                report_data['screenshot_stats'] = self.screenshot_manager.get_screenshot_stats()
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"JSON report generated: {json_file}")
            return json_file
            
        except Exception as e:
            logger.error(f"Failed to generate JSON report: {e}")
            return None
    
    def generate_html_report(self):
        """Generate HTML report with embedded screenshots"""
        html_file = f"{self.report_dir}/html/test_report.html"
        
        try:
            # Calculate additional statistics
            total_tests = len(self.test_results)
            passed_tests = len([r for r in self.test_results if r['result']])
            failed_tests = total_tests - passed_tests
            success_rate = self.stats.get('success_rate', 0)
            
            # Group results by action type for analysis
            action_analysis = {}
            for result in self.test_results:
                action = result['action_type']
                if action not in action_analysis:
                    action_analysis[action] = {'total': 0, 'passed': 0, 'failed': 0}
                
                action_analysis[action]['total'] += 1
                if result['result']:
                    action_analysis[action]['passed'] += 1
                else:
                    action_analysis[action]['failed'] += 1
            
            # Generate HTML content
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QA-Monkey Test Report - {self.session_id}</title>
    <style>
        body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0; font-size: 2.5em; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; margin-bottom: 10px; }}
        .success {{ color: #27ae60; }}
        .danger {{ color: #e74c3c; }}
        .warning {{ color: #f39c12; }}
        .info {{ color: #3498db; }}
        .results-table {{ width: 100%; border-collapse: collapse; }}
        .results-table th, .results-table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        .results-table th {{ background: #f8f9fa; font-weight: bold; }}
        .status-badge {{ padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }}
        .status-success {{ background: #d4edda; color: #155724; }}
        .status-failed {{ background: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐒 QA-Monkey Test Report</h1>
            <p><strong>Session:</strong> {self.session_id}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Framework:</strong> Python-Selenium with POM Design</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number info">{total_tests}</div>
                <div>Total Tests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number success">{passed_tests}</div>
                <div>Passed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number danger">{failed_tests}</div>
                <div>Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number {'success' if success_rate >= 90 else 'warning' if success_rate >= 70 else 'danger'}">{success_rate}%</div>
                <div>Success Rate</div>
            </div>
        </div>
        
        <h2>📊 Action Analysis</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 30px;">
"""
            
            for action, data in action_analysis.items():
                success_pct = (data['passed'] / data['total'] * 100) if data['total'] > 0 else 0
                html_content += f"""
            <div style="border: 1px solid #ddd; border-radius: 6px; padding: 15px; background: white;">
                <div style="font-weight: bold; margin-bottom: 10px; color: #495057;">{action.upper()} Actions</div>
                <p>Total: {data['total']} | Passed: {data['passed']} | Failed: {data['failed']}</p>
                <div style="background: #e9ecef; border-radius: 4px; overflow: hidden; height: 20px;">
                    <div style="height: 100%; background: linear-gradient(90deg, #28a745, #20c997); width: {success_pct}%;"></div>
                </div>
                <small>{success_pct:.1f}% success rate</small>
            </div>
"""
            
            html_content += """
        </div>
        
        <h2>🔍 Detailed Test Results</h2>
        <table class="results-table">
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Action</th>
                    <th>Element</th>
                    <th>Status</th>
                    <th>Error</th>
                </tr>
            </thead>
            <tbody>
"""
            
            for result in self.test_results[:50]:  # Limit to first 50 for readability
                timestamp = result['timestamp'].split('T')[1][:8]
                status_class = 'status-success' if result['result'] else 'status-failed'
                error_msg = result.get('error_msg', '')[:60] if result.get('error_msg') else '-'
                
                html_content += f"""
                <tr>
                    <td>{timestamp}</td>
                    <td><strong>{result['action_type'].upper()}</strong></td>
                    <td>{result['element_info'][:50]}</td>
                    <td><span class="status-badge {status_class}">{result['status']}</span></td>
                    <td>{error_msg}</td>
                </tr>
"""
            
            html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML report generated: {html_file}")
            return html_file
            
        except Exception as e:
            logger.error(f"Failed to generate HTML report: {e}")
            return None
    
    def generate_all_reports(self):
        """Generate all report formats"""
        reports = {}
        
        reports['csv'] = self.generate_csv_report()
        reports['json'] = self.generate_json_report()
        reports['html'] = self.generate_html_report()
        
        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['result']])
        success_rate = self.stats.get('success_rate', 0)
        
        summary = f"""
📊 REGRESSION TEST SUMMARY
{'='*50}
Session ID: {self.session_id}
Framework: Python-Selenium with POM Design
Total Tests: {total_tests}
Passed: {passed_tests}
Failed: {total_tests - passed_tests}
Success Rate: {success_rate}%
{'='*50}

📁 Generated Reports:
- CSV: {reports['csv']}
- JSON: {reports['json']}  
- HTML: {reports['html']}
"""
        
        print(summary)
        return reports
import logging
import os
from datetime import datetime
import json

class EnhancedLogger:
    """Enhanced logging system with structured output"""
    
    def __init__(self, session_id, log_level=logging.INFO):
        self.session_id = session_id
        self.setup_directories()
        self.setup_loggers(log_level)
        self.test_results = []
        self.action_stats = {
            'total_actions': 0,
            'successful_actions': 0,
            'failed_actions': 0,
            'errors': 0
        }
    
    def setup_directories(self):
        """Create logging directories"""
        self.log_dir = f"logs/{self.session_id}"
        self.error_dir = f"errors/{self.session_id}"
        
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.error_dir, exist_ok=True)
    
    def setup_loggers(self, log_level):
        """Setup multiple loggers for different purposes"""
        
        # Main application logger
        self.logger = logging.getLogger('qa_monkey')
        self.logger.setLevel(log_level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # File handler for detailed logs
        file_handler = logging.FileHandler(f'{self.log_dir}/detailed.log')
        file_handler.setLevel(log_level)
        file_format = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
        
        # Action logger for structured action logging
        self.action_logger = logging.getLogger('qa_monkey.actions')
        self.action_logger.setLevel(log_level)
        self.action_logger.handlers.clear()
        
        action_handler = logging.FileHandler(f'{self.log_dir}/actions.log')
        action_handler.setLevel(log_level)
        action_format = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        action_handler.setFormatter(action_format)
        self.action_logger.addHandler(action_handler)
    
    def log_action(self, action_type, element_info, result, error_msg=None, screenshot_path=None):
        """Log individual action with detailed information"""
        timestamp = datetime.now().isoformat()
        
        # Update statistics
        self.action_stats['total_actions'] += 1
        if result:
            self.action_stats['successful_actions'] += 1
            status = "SUCCESS"
            level = logging.INFO
        else:
            self.action_stats['failed_actions'] += 1
            status = "FAILED"
            level = logging.WARNING
            
        if error_msg:
            self.action_stats['errors'] += 1
            level = logging.ERROR
        
        # Create log message
        log_msg = f"{action_type.upper()} on {element_info} - {status}"
        if error_msg:
            log_msg += f" - Error: {error_msg}"
        if screenshot_path:
            log_msg += f" - Screenshot: {screenshot_path}"
        
        # Log to action logger
        self.action_logger.log(level, log_msg)
        
        # Store structured result
        result_data = {
            'timestamp': timestamp,
            'action_type': action_type,
            'element_info': element_info,
            'result': result,
            'error_msg': error_msg,
            'screenshot_path': screenshot_path,
            'status': status
        }
        self.test_results.append(result_data)
    
    def log_page_action(self, page_name, action_method, result, error_msg=None):
        """Log page-specific actions"""
        self.logger.info(f"Page: {page_name} - Action: {action_method} - {'SUCCESS' if result else 'FAILED'}")
        if error_msg:
            self.logger.error(f"Page action error: {error_msg}")
    
    def get_stats(self):
        """Get current statistics"""
        total = self.action_stats['total_actions']
        if total > 0:
            success_rate = (self.action_stats['successful_actions'] / total) * 100
        else:
            success_rate = 0
        
        return {
            **self.action_stats,
            'success_rate': round(success_rate, 1)
        }
    
    def save_session_data(self):
        """Save session data to JSON"""
        session_file = f'{self.log_dir}/session_data.json'
        session_data = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'statistics': self.get_stats(),
            'test_results': self.test_results
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        return session_file
class TestConfig:
    """Configuration for monkey testing"""
    
    # Test URLs
    URLS = [
        "https://www.google.com",
        "https://github.com",
        "https://example.com",
        "https://the-internet.herokuapp.com/",
        "https://demoqa.com/elements",
        "https://httpbin.org/forms/post"
    ]
    
    # Test settings
    DEFAULT_ITERATIONS = 20
    MIN_DELAY = 0.5
    MAX_DELAY = 1.5
    PAGE_LOAD_WAIT = 3
    
    # Action weights (probability of selection)
    ACTION_WEIGHTS = {
        "click": 0.4,
        "scroll": 0.3,
        "input": 0.2,
        "hover": 0.1
    }
    
    # Test categories
    TEST_CATEGORIES = {
        "quick": {
            "urls": URLS[:3],
            "iterations": 10
        },
        "comprehensive": {
            "urls": URLS,
            "iterations": 20
        },
        "extended": {
            "urls": URLS,
            "iterations": 30
        }
    }
    
    @classmethod
    def get_test_config(cls, category="comprehensive"):
        """Get test configuration by category"""
        return cls.TEST_CATEGORIES.get(category, cls.TEST_CATEGORIES["comprehensive"])
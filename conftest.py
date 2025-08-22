import pytest
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

@pytest.fixture(scope="session")
def setup_test_environment():
    """Setup test environment for pytest runs"""
    print("Setting up test environment...")
    yield
    print("Tearing down test environment...")

@pytest.fixture
def sample_test_data():
    """Provide sample test data"""
    return {
        'test_urls': [
            'https://example.com',
            'https://httpbin.org/forms/post'
        ],
        'credentials': {
            'username': 'test_user',
            'password': 'test_password'
        },
        'search_queries': [
            'selenium automation',
            'python testing',
            'qa framework'
        ]
    }
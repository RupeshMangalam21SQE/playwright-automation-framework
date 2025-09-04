"""
Configuration settings for the Playwright automation framework
"""

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Central configuration class for the framework"""

    # Base Configuration
    BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
    BROWSER = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # Slow down operations by milliseconds
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Timeouts
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))  # 30 seconds
    NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "10000"))  # 10 seconds

    # Test Data
    VALID_USERNAME = os.getenv("VALID_USERNAME", "standard_user")
    VALID_PASSWORD = os.getenv("VALID_PASSWORD", "secret_sauce")
    INVALID_USERNAME = os.getenv("INVALID_USERNAME", "invalid_user")
    INVALID_PASSWORD = os.getenv("INVALID_PASSWORD", "invalid_password")

    # Directory Paths
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
    SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")
    TEST_DATA_DIR = os.path.join(PROJECT_ROOT, "test_data")

    # API Configuration
    API_BASE_URL = os.getenv("API_BASE_URL", "https://reqres.in/api")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))

    # Parallel Execution
    PARALLEL_WORKERS = int(os.getenv("PARALLEL_WORKERS", "4"))

    # Retry Configuration
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "1"))

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Browser specific settings
    BROWSER_ARGS = {
        "chromium": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-extensions",
            "--disable-plugins",
            (
                "--disable-images"
                if os.getenv("DISABLE_IMAGES", "False").lower() == "true"
                else ""
            ),
        ],
        "firefox": [
            "--width=1920",
            "--height=1080",
        ],
        "webkit": [],
    }

    # CI/CD Configuration
    CI_ENVIRONMENT = os.getenv("CI", "False").lower() == "true"
    GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS", "False").lower() == "true"

    # Test Environment URLs
    ENVIRONMENTS = {
        "dev": "https://dev.saucedemo.com/",
        "staging": "https://staging.saucedemo.com/",
        "prod": "https://www.saucedemo.com/",
    }

    CURRENT_ENV = os.getenv("TEST_ENVIRONMENT", "prod")

    @classmethod
    def get_base_url(cls):
        """Get base URL based on current environment"""
        return cls.ENVIRONMENTS.get(cls.CURRENT_ENV, cls.BASE_URL)

    @classmethod
    def get_browser_args(cls):
        """Get browser-specific arguments"""
        args = cls.BROWSER_ARGS.get(cls.BROWSER, [])
        return [arg for arg in args if arg]  # Filter out empty strings

    @classmethod
    def is_ci_environment(cls):
        """Check if running in CI environment"""
        return cls.CI_ENVIRONMENT or cls.GITHUB_ACTIONS

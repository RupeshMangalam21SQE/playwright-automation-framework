"""
Pytest Configuration and Fixtures for Playwright Framework (Maximized Window)
"""

import os
from datetime import datetime
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from utils.config import Config
from utils.helpers import ScreenshotHelper, TestDataManager


# -----------------------
# Browser / Context Setup
# -----------------------

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args) -> dict:
    """
    Ensure the browser launches with a large, desktop-like viewport (even if headless).
    """
    args = ["--start-maximized", "--window-size=1920,1080"]
    return {**browser_type_launch_args, "headless": Config.HEADLESS, "args": args}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args) -> dict:
    """
    Force all contexts to use a large desktop viewport.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def browser(pytestconfig) -> Generator[Browser, None, None]:
    """
    Launch browser for session.
    """
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser_instance = p.chromium.launch(
            headless=Config.HEADLESS, args=["--start-maximized", "--window-size=1920,1080"]
        )
        yield browser_instance
        browser_instance.close()


@pytest.fixture(scope="session")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Provide a new browser context for the session.
    """
    context_instance = browser.new_context(
        viewport={"width": 1920, "height": 1080}, ignore_https_errors=True
    )
    yield context_instance
    context_instance.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Provide a new page for each test function.
    """
    page = context.new_page()
    page.set_default_timeout(Config.DEFAULT_TIMEOUT)

    if Config.DEBUG:
        page.on("console", lambda msg: print(f"Console: {msg.text}"))
        page.on("pageerror", lambda error: print(f"Page Error: {error}"))

    yield page
    page.close()


# -----------------------
# Helpers / Test Data
# -----------------------

@pytest.fixture(scope="function")
def test_data() -> TestDataManager:
    return TestDataManager()


@pytest.fixture(scope="function")
def screenshot_helper(page: Page) -> ScreenshotHelper:
    return ScreenshotHelper(page)


# -----------------------
# Automatic Screenshot on Failure
# -----------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_dir = os.path.join(Config.SCREENSHOTS_DIR)
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(
                screenshot_dir, f"{item.name}_{timestamp}.png"
            )
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")


# -----------------------
# Test Environment Setup
# -----------------------

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    os.makedirs(Config.REPORTS_DIR, exist_ok=True)
    os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
    print("Test environment setup completed")
    print(f"Base URL: {Config.BASE_URL}")
    print(f"Browser: {Config.BROWSER}")
    print(f"Headless: {Config.HEADLESS}")
    yield
    print("Test environment cleanup completed")


# -----------------------
# Pytest Marker Configuration
# -----------------------

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: marks tests as smoke tests")
    config.addinivalue_line("markers", "regression: marks tests as regression tests")
    config.addinivalue_line("markers", "api: marks tests as API tests")
    config.addinivalue_line("markers", "ui: marks tests as UI tests")
    config.addinivalue_line("markers", "login: marks tests related to login functionality")
    config.addinivalue_line("markers", "shopping: marks tests related to shopping functionality")
    config.addinivalue_line("markers", "slow: marks tests as slow running tests")


# -----------------------
# Page Object Fixtures
# -----------------------

@pytest.fixture(scope="session")
def login_page(page: Page):
    from pages.login_page import LoginPage
    return LoginPage(page)


@pytest.fixture(scope="session")
def home_page(page: Page):
    from pages.home_page import HomePage
    return HomePage(page)


@pytest.fixture(scope="session")
def product_page(page: Page):
    from pages.product_page import ProductPage
    return ProductPage(page)

@pytest.fixture(scope="session")
def cart_page(page: Page):
    from pages.cart_page import CartPage
    return CartPage(page)

"""
Base Page Object class for Playwright framework
Contains common functionality shared across all page objects
"""

from playwright.sync_api import Page, Locator
from typing import Optional, List
import logging
from utils.config import Config
from abc import ABC, abstractmethod


class BasePage(ABC):
    """Base page object class with common functionality"""
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)
        self.timeout = Config.DEFAULT_TIMEOUT
    
    @abstractmethod
    def get_page_url(self) -> str:
        """Abstract method to return the page URL"""
        pass
    
    @abstractmethod
    def get_page_title(self) -> str:
        """Abstract method to return expected page title"""
        pass
    
    def navigate_to(self, url: Optional[str] = None) -> None:
        """Navigate to the page URL"""
        target_url = url or self.get_page_url()
        self.logger.info(f"Navigating to: {target_url}")
        self.page.goto(target_url, wait_until="networkidle", timeout=Config.NAVIGATION_TIMEOUT)
    
    def get_current_url(self) -> str:
        """Get the current page URL"""
        return self.page.url
    
    def get_title(self) -> str:
        """Get the current page title"""
        return self.page.title()
    
    def wait_for_page_load(self) -> None:
        """Wait for the page to fully load"""
        self.page.wait_for_load_state("networkidle", timeout=self.timeout)
    
    def wait_for_element(self, locator: str, state: str = "visible") -> Locator:
        """Wait for element to be in specified state"""
        element = self.page.locator(locator)
        element.wait_for(state=state, timeout=self.timeout)
        return element
    
    def click_element(self, locator: str, force: bool = False) -> None:
        """Click on an element with optional force click"""
        self.logger.info(f"Clicking element: {locator}")
        element = self.wait_for_element(locator, "visible")
        element.click(force=force)
    
    def fill_input(self, locator: str, text: str, clear_first: bool = True) -> None:
        """Fill input field with text"""
        self.logger.info(f"Filling input {locator} with: {text}")
        element = self.wait_for_element(locator, "visible")
        if clear_first:
            element.clear()
        element.fill(text)
    
    def get_text(self, locator: str) -> str:
        """Get text content of an element"""
        element = self.wait_for_element(locator, "visible")
        return element.text_content() or ""
    
    def get_attribute(self, locator: str, attribute: str) -> Optional[str]:
        """Get attribute value of an element"""
        element = self.wait_for_element(locator, "visible")
        return element.get_attribute(attribute)
    
    def is_element_visible(self, locator: str, timeout: int = 5000) -> bool:
        """Check if element is visible"""
        try:
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
    
    def is_element_enabled(self, locator: str) -> bool:
        """Check if element is enabled"""
        element = self.page.locator(locator)
        return element.is_enabled()
    
    def select_dropdown_option(self, locator: str, option: str, by: str = "value") -> None:
        """Select dropdown option by value, text, or index"""
        self.logger.info(f"Selecting dropdown option: {option} by {by}")
        element = self.wait_for_element(locator, "visible")
        
        if by == "value":
            element.select_option(value=option)
        elif by == "text":
            element.select_option(label=option)
        elif by == "index":
            element.select_option(index=int(option))
    
    def hover_element(self, locator: str) -> None:
        """Hover over an element"""
        self.logger.info(f"Hovering over element: {locator}")
        element = self.wait_for_element(locator, "visible")
        element.hover()
    
    def press_key(self, key: str, locator: Optional[str] = None) -> None:
        """Press keyboard key on element or page"""
        if locator:
            element = self.wait_for_element(locator, "visible")
            element.press(key)
        else:
            self.page.keyboard.press(key)
    
    def take_screenshot(self, filename: Optional[str] = None, full_page: bool = True) -> str:
        """Take screenshot of the page"""
        import os
        from datetime import datetime
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        screenshot_path = os.path.join(Config.SCREENSHOTS_DIR, filename)
        os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
        
        self.page.screenshot(path=screenshot_path, full_page=full_page)
        self.logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    
    def get_element_count(self, locator: str) -> int:
        """Get count of elements matching locator"""
        elements = self.page.locator(locator)
        return elements.count()
    
    def get_all_text_contents(self, locator: str) -> List[str]:
        """Get text content of all matching elements"""
        elements = self.page.locator(locator)
        return elements.all_text_contents()
    
    def verify_page_title(self, expected_title: Optional[str] = None) -> None:
        """Verify current page title matches expected"""
        expected = expected_title or self.get_page_title()
        actual = self.get_title()
        assert expected in actual, f"Expected title '{expected}' not found in '{actual}'"
    
    def verify_current_url(self, expected_url: Optional[str] = None) -> None:
        """Verify current URL contains expected URL"""
        expected = expected_url or self.get_page_url()
        actual = self.get_current_url()
        assert expected in actual, f"Expected URL '{expected}' not found in '{actual}'"
    
    def wait_for_url_change(self, timeout: int = 30000) -> None:
        """Wait for URL to change"""
        current_url = self.get_current_url()
        self.page.wait_for_url(lambda url: url != current_url, timeout=timeout)

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage
from utils.config import Config
import time


class LoginPage(BasePage):
    """Login page object for SauceDemo"""

    # ---------------- Locators ----------------
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"
    LOGIN_LOGO = ".login_logo"

    STANDARD_USER = "standard_user"
    VALID_PASSWORD = "secret_sauce"

    # ---------------- Methods ----------------
    def login_with_standard_user(self) -> None:
        """Login with standard user with retries"""
        retries = 3
        for _ in range(retries):
            try:
                self.enter_username(self.STANDARD_USER)
                self.enter_password(self.VALID_PASSWORD)
                self.click_element(self.LOGIN_BUTTON, timeout=3000)
                self.wait_for_url_change(timeout=5000)
                return
            except PlaywrightTimeoutError:
                time.sleep(1)
        raise Exception("Login failed after multiple attempts")

    def enter_username(self, username: str) -> None:
        """Enter username with wait"""
        self.wait_for_element(self.USERNAME_INPUT, timeout=3000)
        self.fill_input(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """Enter password with wait"""
        self.wait_for_element(self.PASSWORD_INPUT, timeout=3000)
        self.fill_input(self.PASSWORD_INPUT, password)

    def verify_login_page_loaded(self) -> None:
        """Verify login page with waits"""
        self.verify_current_url()
        assert self.wait_for_element(self.LOGIN_LOGO, timeout=5000), "Login logo not visible"
        assert self.wait_for_element(self.USERNAME_INPUT, timeout=5000), "Username field not visible"
        assert self.wait_for_element(self.PASSWORD_INPUT, timeout=5000), "Password field not visible"

"""
Login Page Object for SauceDemo application
"""

from typing import Optional

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.config import Config


class LoginPage(BasePage):
    """Login page object for SauceDemo"""

    def __init__(self, page: Page):
        super().__init__(page)

    # Page URL and Title
    def get_page_url(self) -> str:
        return f"{Config.get_base_url()}"

    def get_page_title(self) -> str:
        return "Swag Labs"

    # Locators
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_BUTTON = ".error-button"
    LOGIN_LOGO = ".login_logo"
    LOGIN_WRAPPER = "#login_button_container"

    # User credentials for different test scenarios
    STANDARD_USER = "standard_user"
    LOCKED_OUT_USER = "locked_out_user"
    PROBLEM_USER = "problem_user"
    PERFORMANCE_GLITCH_USER = "performance_glitch_user"
    VALID_PASSWORD = "secret_sauce"

    def navigate_to_login(self) -> None:
        """Navigate to login page"""
        self.navigate_to()
        self.wait_for_page_load()

    def enter_username(self, username: str) -> None:
        """Enter username in the username field"""
        self.fill_input(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """Enter password in the password field"""
        self.fill_input(self.PASSWORD_INPUT, password)

    def click_login_button(self) -> None:
        """Click the login button"""
        self.click_element(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Complete login flow with credentials"""
        self.logger.info(f"Logging in with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def login_with_valid_credentials(self) -> None:
        """Login with default valid credentials"""
        self.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    def login_with_standard_user(self) -> None:
        """Login with standard user credentials"""
        self.login(self.STANDARD_USER, self.VALID_PASSWORD)

    def login_with_problem_user(self) -> None:
        """Login with problem user credentials"""
        self.login(self.PROBLEM_USER, self.VALID_PASSWORD)

    def login_with_performance_user(self) -> None:
        """Login with performance glitch user credentials"""
        self.login(self.PERFORMANCE_GLITCH_USER, self.VALID_PASSWORD)

    def login_with_locked_user(self) -> None:
        """Login with locked out user credentials"""
        self.login(self.LOCKED_OUT_USER, self.VALID_PASSWORD)

    def get_error_message(self) -> str:
        """Get the error message text"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE)

    def clear_error_message(self) -> None:
        """Click the error button to clear error message"""
        if self.is_element_visible(self.ERROR_BUTTON):
            self.click_element(self.ERROR_BUTTON)

    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled"""
        return self.is_element_enabled(self.LOGIN_BUTTON)

    def is_login_form_visible(self) -> bool:
        """Check if login form is visible"""
        return (
            self.is_element_visible(self.USERNAME_INPUT)
            and self.is_element_visible(self.PASSWORD_INPUT)
            and self.is_element_visible(self.LOGIN_BUTTON)
        )

    def get_username_placeholder(self) -> str:
        """Get username input placeholder text"""
        return self.get_attribute(self.USERNAME_INPUT, "placeholder") or ""

    def get_password_placeholder(self) -> str:
        """Get password input placeholder text"""
        return self.get_attribute(self.PASSWORD_INPUT, "placeholder") or ""

    def clear_login_form(self) -> None:
        """Clear both username and password fields"""
        self.fill_input(self.USERNAME_INPUT, "")
        self.fill_input(self.PASSWORD_INPUT, "")

    def verify_login_page_loaded(self) -> None:
        """Verify that login page has loaded correctly"""
        self.verify_current_url()
        self.verify_page_title()
        assert self.is_login_form_visible(), "Login form is not visible"
        assert self.is_element_visible(self.LOGIN_LOGO), "Login logo is not visible"

    def verify_successful_login(self) -> None:
        """Verify that login was successful by checking URL change"""
        self.wait_for_url_change()
        current_url = self.get_current_url()
        assert (
            "inventory.html" in current_url
        ), f"Login failed - still on login page: {current_url}"

    def verify_login_error(self, expected_error: str) -> None:
        """Verify that specific login error is displayed"""
        assert self.is_error_displayed(), "No error message is displayed"
        actual_error = self.get_error_message()
        assert (
            expected_error in actual_error
        ), f"Expected error '{expected_error}' not found in '{actual_error}'"

    def verify_locked_out_error(self) -> None:
        """Verify locked out user error message"""
        expected_error = "Sorry, this user has been locked out"
        self.verify_login_error(expected_error)

    def verify_invalid_credentials_error(self) -> None:
        """Verify invalid credentials error message"""
        expected_error = "Username and password do not match any user"
        self.verify_login_error(expected_error)

    def perform_login_with_keyboard(self, username: str, password: str) -> None:
        """Perform login using keyboard navigation"""
        self.enter_username(username)
        self.press_key("Tab", self.USERNAME_INPUT)
        self.enter_password(password)
        self.press_key("Enter", self.PASSWORD_INPUT)

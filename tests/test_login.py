"""
Test cases for Login functionality using Playwright framework
"""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.config import Config
from utils.test_data import LoginTestData


class TestLogin:
    """Test class for login functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test"""
        self.login_page = LoginPage(page)
        self.home_page = HomePage(page)
        self.login_page.navigate_to_login()
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_successful_login_standard_user(self):
        """Test successful login with standard user credentials"""
        # Arrange
        username = "standard_user"
        password = "secret_sauce"
        
        # Act
        self.login_page.login(username, password)
        
        # Assert
        self.login_page.verify_successful_login()
        self.home_page.verify_home_page_loaded()
        
        # Verify user can see products
        assert self.home_page.get_product_count() > 0, "No products displayed after login"
        
        # Verify cart is accessible
        assert self.home_page.get_cart_item_count() == 0, "Cart should be empty initially"
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_with_invalid_username(self):
        """Test login with invalid username"""
        # Arrange
        username = "invalid_user"
        password = "secret_sauce"
        
        # Act
        self.login_page.login(username, password)
        
        # Assert
        self.login_page.verify_invalid_credentials_error()
        assert self.login_page.get_current_url() == self.login_page.get_page_url()
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_with_invalid_password(self):
        """Test login with invalid password"""
        # Arrange
        username = "standard_user"
        password = "invalid_password"
        
        # Act
        self.login_page.login(username, password)
        
        # Assert
        self.login_page.verify_invalid_credentials_error()
        assert self.login_page.get_current_url() == self.login_page.get_page_url()
    
    @pytest.mark.login
    def test_login_with_empty_credentials(self):
        """Test login with empty username and password"""
        # Act
        self.login_page.click_login_button()
        
        # Assert
        expected_error = "Username is required"
        self.login_page.verify_login_error(expected_error)
    
    @pytest.mark.login
    def test_login_with_locked_out_user(self):
        """Test login with locked out user"""
        # Arrange
        username = "locked_out_user"
        password = "secret_sauce"
        
        # Act
        self.login_page.login(username, password)
        
        # Assert
        self.login_page.verify_locked_out_error()
    
    @pytest.mark.login
    def test_login_form_elements_visibility(self):
        """Test that all login form elements are visible"""
        # Assert
        assert self.login_page.is_login_form_visible(), "Login form is not visible"
        assert self.login_page.is_element_visible(self.login_page.LOGIN_LOGO), "Login logo is not visible"
        assert self.login_page.is_login_button_enabled(), "Login button is not enabled"
    
    @pytest.mark.login
    @pytest.mark.parametrize("username,password,expected_result", [
        ("standard_user", "secret_sauce", "success"),
        ("locked_out_user", "secret_sauce", "locked_out"),
        ("problem_user", "secret_sauce", "success"),
        ("performance_glitch_user", "secret_sauce", "success"),
        ("invalid_user", "secret_sauce", "invalid_credentials"),
        ("standard_user", "invalid_password", "invalid_credentials"),
        ("", "secret_sauce", "username_required"),
        ("standard_user", "", "password_required"),
    ])
    def test_login_scenarios_parameterized(self, username, password, expected_result):
        """Parameterized test for different login scenarios"""
        # Act
        self.login_page.login(username, password)
        
        # Assert based on expected result
        if expected_result == "success":
            self.login_page.verify_successful_login()
            self.home_page.verify_home_page_loaded()
        elif expected_result == "locked_out":
            self.login_page.verify_locked_out_error()
        elif expected_result == "invalid_credentials":
            self.login_page.verify_invalid_credentials_error()
        elif expected_result == "username_required":
            self.login_page.verify_login_error("Username is required")
        elif expected_result == "password_required":
            self.login_page.verify_login_error("Password is required")
    
    @pytest.mark.login
    def test_keyboard_navigation_login(self):
        """Test login using keyboard navigation"""
        # Arrange
        username = "standard_user"
        password = "secret_sauce"
        
        # Act - login using keyboard
        self.login_page.perform_login_with_keyboard(username, password)
        
        # Assert
        self.login_page.verify_successful_login()
        self.home_page.verify_home_page_loaded()


class TestLoginDataDriven:
    """Data-driven login tests using external test data"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, test_data):
        """Setup for data-driven tests"""
        self.login_page = LoginPage(page)
        self.home_page = HomePage(page)
        self.test_data = test_data
        self.login_page.navigate_to_login()
    
    @pytest.mark.login
    def test_login_with_test_data(self):
        """Test login using data from test data manager"""
        test_cases = self.test_data.get_login_test_cases()
        
        for test_case in test_cases:
            username = test_case['username']
            password = test_case['password']
            expected_result = test_case['expected_result']
            
            # Clear form before next test
            self.login_page.clear_login_form()
            
            # Perform login
            self.login_page.login(username, password)
            
            # Verify result based on expected outcome
            if expected_result == "success":
                self.login_page.verify_successful_login()
                # Logout for next iteration
                self.home_page.logout()
            else:
                assert self.login_page.is_error_displayed(), f"Error should be displayed for {username}/{password}"

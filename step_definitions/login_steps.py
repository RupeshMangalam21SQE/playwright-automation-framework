"""
Step definitions for login feature using pytest-bdd
"""

import pytest
from playwright.sync_api import Page
from pytest_bdd import given, parsers, scenarios, then, when

from pages.home_page import HomePage
from pages.login_page import LoginPage

# Load scenarios from the feature file
scenarios("../features/login.feature")


@pytest.fixture
def login_page(page: Page):
    """Fixture to provide login page object"""
    return LoginPage(page)


@pytest.fixture
def home_page(page: Page):
    """Fixture to provide home page object"""
    return HomePage(page)


@pytest.fixture
def context_data():
    """Fixture to store test context data"""
    return {}


@given("I am on the login page")
def navigate_to_login_page(login_page: LoginPage):
    """Navigate to the login page"""
    login_page.navigate_to_login()
    login_page.verify_login_page_loaded()


@when("I enter valid credentials")
def enter_valid_credentials(login_page: LoginPage):
    """Enter valid login credentials"""
    login_page.login_with_standard_user()


@when("I enter an invalid username and valid password")
def enter_invalid_username(login_page: LoginPage):
    """Enter invalid username with valid password"""
    login_page.login("invalid_user", "secret_sauce")


@when("I enter a valid username and invalid password")
def enter_invalid_password(login_page: LoginPage):
    """Enter valid username with invalid password"""
    login_page.login("standard_user", "invalid_password")


@when("I enter locked out user credentials")
def enter_locked_out_credentials(login_page: LoginPage):
    """Enter locked out user credentials"""
    login_page.login_with_locked_user()


@when("I click the login button without entering credentials")
def click_login_without_credentials(login_page: LoginPage):
    """Click login button with empty credentials"""
    login_page.click_login_button()


@when(parsers.parse('I login with "{username}" and "{password}"'))
def login_with_credentials(
    login_page: LoginPage, username: str, password: str, context_data: dict
):
    """Login with specified credentials and store context"""
    context_data["username"] = username
    context_data["password"] = password
    login_page.login(username, password)


@then("I should be redirected to the home page")
def verify_redirect_to_home_page(login_page: LoginPage):
    """Verify successful redirect to home page"""
    login_page.verify_successful_login()


@then("I should see the product inventory")
def verify_product_inventory(home_page: HomePage):
    """Verify product inventory is visible"""
    home_page.verify_home_page_loaded()
    assert home_page.get_product_count() > 0, "No products are visible"


@then(parsers.parse('I should see an error message "{error_message}"'))
def verify_error_message(login_page: LoginPage, error_message: str):
    """Verify specific error message is displayed"""
    login_page.verify_login_error(error_message)


@then("I should remain on the login page")
def verify_remain_on_login_page(login_page: LoginPage):
    """Verify user remains on login page"""
    current_url = login_page.get_current_url()
    expected_url = login_page.get_page_url()
    assert (
        expected_url in current_url
    ), f"Expected to remain on login page, but current URL is {current_url}"


@then(parsers.parse('the login result should be "{result}"'))
def verify_login_result(
    login_page: LoginPage, home_page: HomePage, result: str, context_data: dict
):
    """Verify the login result based on expected outcome"""
    username = context_data.get("username", "")

    if result == "success":
        login_page.verify_successful_login()
        home_page.verify_home_page_loaded()
        # Logout for next test iteration
        home_page.logout()
    elif result == "locked_out":
        login_page.verify_locked_out_error()
    elif result == "invalid_credentials":
        login_page.verify_invalid_credentials_error()
    else:
        raise ValueError(f"Unknown result type: {result}")

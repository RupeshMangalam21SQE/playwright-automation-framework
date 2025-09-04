"""
Step definitions for shopping feature using pytest-bdd
"""

import pytest
from playwright.sync_api import Page
from pytest_bdd import given, parsers, scenarios, then, when

from pages.home_page import HomePage
from pages.login_page import LoginPage

# Load scenarios from the feature file
scenarios("../features/shopping.feature")


@pytest.fixture
def context_data():
    """Fixture to store test context data"""
    return {}


@given("I am logged in as a standard user")
def login_as_standard_user(login_page: LoginPage):
    """Login as standard user"""
    login_page.navigate_to_login()
    login_page.login_with_standard_user()


@given("I am on the home page")
def verify_on_home_page(home_page: HomePage):
    """Verify user is on home page"""
    home_page.verify_home_page_loaded()


@given(parsers.parse('I have "{product_name}" in the cart'))
def add_product_to_cart_setup(home_page: HomePage, product_name: str):
    """Add product to cart for setup"""
    home_page.add_product_to_cart_by_name(product_name)
    assert home_page.is_product_in_cart(
        product_name
    ), f"{product_name} should be in cart"


@when(parsers.parse('I add "{product_name}" to the cart'))
def add_product_to_cart(home_page: HomePage, product_name: str):
    """Add specified product to cart"""
    home_page.add_product_to_cart_by_name(product_name)


@when("I add the following products to the cart:")
def add_multiple_products_to_cart(home_page: HomePage, datatable):
    """Add multiple products to cart"""
    products = [row[0] for row in datatable]
    for product in products:
        home_page.add_product_to_cart_by_name(product)


@when(parsers.parse('I remove "{product_name}" from the cart'))
def remove_product_from_cart(home_page: HomePage, product_name: str):
    """Remove specified product from cart"""
    home_page.remove_product_from_cart_by_name(product_name)


@when(parsers.parse('I sort products by "{sort_option}"'))
def sort_products(home_page: HomePage, sort_option: str):
    """Sort products by specified option"""
    if sort_option == "Name (A to Z)":
        home_page.sort_products(home_page.SORT_NAME_ASC)
    elif sort_option == "Name (Z to A)":
        home_page.sort_products(home_page.SORT_NAME_DESC)


@when("I click on the shopping cart")
def click_shopping_cart(home_page: HomePage):
    """Click on shopping cart"""
    home_page.click_shopping_cart()


@then("the product should be in the cart")
def verify_product_in_cart(home_page: HomePage):
    """Verify product is in cart"""
    # This would need to be more specific in real implementation
    assert home_page.get_cart_item_count() > 0, "Cart should not be empty"


@then("all products should be in the cart")
def verify_all_products_in_cart(home_page: HomePage):
    """Verify all products are in cart"""
    assert home_page.get_cart_item_count() == 3, "Should have 3 products in cart"


@then("the product should not be in the cart")
def verify_product_not_in_cart(home_page: HomePage):
    """Verify product is not in cart"""
    assert home_page.get_cart_item_count() == 0, "Cart should be empty"


@then(parsers.parse('the cart badge should show "{count}"'))
def verify_cart_badge_count(home_page: HomePage, count: str):
    """Verify cart badge shows correct count"""
    expected_count = int(count)
    home_page.verify_cart_badge_count(expected_count)


@then("products should be sorted alphabetically ascending")
def verify_products_sorted_asc(home_page: HomePage):
    """Verify products are sorted A-Z"""
    home_page.verify_products_sorted_by_name_asc()


@then("products should be sorted alphabetically descending")
def verify_products_sorted_desc(home_page: HomePage):
    """Verify products are sorted Z-A"""
    home_page.verify_products_sorted_by_name_desc()


@then("I should be on the cart page")
def verify_on_cart_page(home_page: HomePage):
    """Verify user is on cart page"""
    current_url = home_page.get_current_url()
    assert (
        "cart.html" in current_url
    ), f"Should be on cart page, but current URL is {current_url}"


@then(parsers.parse("I should see {count:d} items in the cart"))
def verify_items_in_cart(home_page: HomePage, count: int):
    """Verify number of items in cart"""
    # This would need cart page implementation for full verification
    assert (
        home_page.get_cart_item_count() == count
    ), f"Should have {count} items in cart"

"""
End-to-End Shopping Test Cases
"""

import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from utils.test_data import CheckoutTestData, ProductTestData


class TestE2EShopping:
    """End-to-end shopping test scenarios"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test - login first"""
        self.login_page = LoginPage(page)
        self.home_page = HomePage(page)
        self.product_page = ProductPage(page)

        # Login before each test
        self.login_page.navigate_to_login()
        self.login_page.login_with_standard_user()
        self.home_page.verify_home_page_loaded()

    @pytest.mark.smoke
    @pytest.mark.shopping
    def test_add_single_product_to_cart(self):
        """Test adding a single product to cart"""
        # Arrange
        product_name = "Sauce Labs Backpack"

        # Act
        self.home_page.add_product_to_cart_by_name(product_name)

        # Assert
        assert self.home_page.is_product_in_cart(
            product_name
        ), f"{product_name} should be in cart"
        self.home_page.verify_cart_badge_count(1)

    @pytest.mark.regression
    @pytest.mark.shopping
    def test_add_multiple_products_to_cart(self):
        """Test adding multiple products to cart"""
        # Arrange
        products = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt",
        ]

        # Act
        for product in products:
            self.home_page.add_product_to_cart_by_name(product)

        # Assert
        for product in products:
            assert self.home_page.is_product_in_cart(
                product
            ), f"{product} should be in cart"

        self.home_page.verify_cart_badge_count(len(products))

    @pytest.mark.shopping
    def test_remove_product_from_cart(self):
        """Test removing a product from cart"""
        # Arrange - Add product first
        product_name = "Sauce Labs Backpack"
        self.home_page.add_product_to_cart_by_name(product_name)
        assert self.home_page.is_product_in_cart(product_name)

        # Act
        self.home_page.remove_product_from_cart_by_name(product_name)

        # Assert
        assert not self.home_page.is_product_in_cart(
            product_name
        ), f"{product_name} should not be in cart"
        self.home_page.verify_cart_badge_count(0)

    @pytest.mark.shopping
    def test_product_sorting_by_name(self):
        """Test product sorting functionality"""
        # Test sort A-Z
        self.home_page.sort_products(self.home_page.SORT_NAME_ASC)
        self.home_page.verify_products_sorted_by_name_asc()

        # Test sort Z-A
        self.home_page.sort_products(self.home_page.SORT_NAME_DESC)
        self.home_page.verify_products_sorted_by_name_desc()

    @pytest.mark.shopping
    def test_product_detail_navigation(self):
        """Test navigation to product detail page"""
        # Arrange
        product_name = "Sauce Labs Backpack"

        # Act
        self.home_page.click_product_name(product_name)

        # Assert
        self.product_page.verify_product_page_loaded()
        product_details = self.product_page.get_product_details()
        assert product_name in product_details["name"], "Product name should match"

    @pytest.mark.regression
    @pytest.mark.shopping
    def test_complete_shopping_workflow(self):
        """Test complete shopping workflow from login to cart"""
        # Add products to cart
        products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
        self.home_page.add_multiple_products_to_cart(products)

        # Verify products in cart
        self.home_page.verify_cart_badge_count(len(products))

        # Navigate to cart
        self.home_page.click_shopping_cart()

        # Verify cart page (would need CartPage object for full implementation)
        assert "cart.html" in self.home_page.get_current_url(), "Should be on cart page"

    @pytest.mark.shopping
    def test_product_information_accuracy(self):
        """Test that product information is displayed correctly"""
        # Get product info from listing page
        product_info = self.home_page.get_product_info(0)  # First product
        product_name = product_info["name"]

        # Navigate to product detail page
        self.home_page.click_product_name(product_name)

        # Get detailed product info
        detailed_info = self.product_page.get_product_details()

        # Assert information matches
        assert (
            product_info["name"] == detailed_info["name"]
        ), "Product names should match"
        assert (
            product_info["price"] == detailed_info["price"]
        ), "Product prices should match"

    @pytest.mark.shopping
    def test_shopping_cart_persistence(self):
        """Test that cart contents persist during session"""
        # Add product to cart
        product_name = "Sauce Labs Backpack"
        self.home_page.add_product_to_cart_by_name(product_name)

        # Navigate away and back
        self.home_page.click_product_name(product_name)
        self.product_page.back_to_products()

        # Verify product still in cart
        assert self.home_page.is_product_in_cart(
            product_name
        ), "Product should persist in cart"
        self.home_page.verify_cart_badge_count(1)

    @pytest.mark.shopping
    @pytest.mark.slow
    def test_performance_with_all_products(self):
        """Test adding all products to cart (performance test)"""
        import time

        start_time = time.time()

        # Get all product names
        product_names = self.home_page.get_product_names()

        # Add all products to cart
        for product_name in product_names:
            self.home_page.add_product_to_cart_by_name(product_name)

        end_time = time.time()
        execution_time = end_time - start_time

        # Assert performance and functionality
        assert (
            execution_time < 30
        ), f"Adding all products took too long: {execution_time:.2f} seconds"
        self.home_page.verify_cart_badge_count(len(product_names))

        # Log performance metrics
        print(f"Added {len(product_names)} products in {execution_time:.2f} seconds")

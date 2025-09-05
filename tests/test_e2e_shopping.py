import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


class TestE2EShopping:
    """End-to-end shopping test scenarios"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup for each test - login first"""
        self.login_page = LoginPage(page)
        self.home_page = HomePage(page)
        self.product_page = ProductPage(page)
        self.cart_page = CartPage(page)

        # Login before each test
        self.login_page.navigate_to_login()
        self.login_page.login_with_standard_user()
        self.home_page.verify_home_page_loaded()

    @pytest.mark.shopping
    def test_add_single_product_to_cart(self):
        product_name = "Sauce Labs Backpack"
        self.home_page.add_product_to_cart_by_name(product_name)
        self.home_page.verify_cart_badge_count(1)

        self.home_page.click_shopping_cart()
        self.cart_page.verify_cart_page_loaded()
        cart_items = self.cart_page.get_cart_item_names()
        assert product_name in cart_items, f"{product_name} should be in cart"

    @pytest.mark.shopping
    def test_add_multiple_products_to_cart(self):
        products = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        self.home_page.add_multiple_products_to_cart(products)
        self.home_page.verify_cart_badge_count(len(products))

        self.home_page.click_shopping_cart()
        self.cart_page.verify_cart_page_loaded()

        cart_items = self.cart_page.get_cart_item_names()
        for product in products:
            assert product in cart_items, f"{product} should be in cart"

    @pytest.mark.shopping
    def test_remove_product_from_cart(self):
        product_name = "Sauce Labs Backpack"
        self.home_page.add_product_to_cart_by_name(product_name)
        self.home_page.click_shopping_cart()
        self.cart_page.verify_cart_page_loaded()

        self.cart_page.remove_item_by_name(product_name)

        cart_items = self.cart_page.get_cart_item_names()
        assert product_name not in cart_items, f"{product_name} should not be in cart"
        assert self.cart_page.get_cart_item_count() == 0, "Cart should be empty"

    @pytest.mark.shopping
    def test_shopping_cart_persistence(self):
        product_name = "Sauce Labs Backpack"
        self.home_page.add_product_to_cart_by_name(product_name)

        # Navigate away and back
        self.home_page.click_product_name(product_name)
        self.product_page.back_to_products()
        self.home_page.click_shopping_cart()
        self.cart_page.verify_cart_page_loaded()

        cart_items = self.cart_page.get_cart_item_names()
        assert product_name in cart_items, f"{product_name} should persist in cart"
        assert self.cart_page.get_cart_item_count() == 1

    @pytest.mark.shopping
    def test_product_sorting_by_name(self):
        # Sort A-Z
        self.home_page.sort_products(self.home_page.SORT_NAME_ASC)
        self.home_page.verify_products_sorted_by_name_asc()

        # Sort Z-A
        self.home_page.sort_products(self.home_page.SORT_NAME_DESC)
        self.home_page.verify_products_sorted_by_name_desc()

    @pytest.mark.shopping
    def test_product_detail_navigation(self):
        product_name = "Sauce Labs Backpack"
        self.home_page.click_product_name(product_name)

        self.product_page.verify_product_page_loaded()
        product_details = self.product_page.get_product_details()
        assert product_name in product_details["name"], "Product name should match"

        # Back to home page
        self.product_page.back_to_products()
        self.home_page.verify_home_page_loaded()

    @pytest.mark.regression
    @pytest.mark.shopping
    def test_complete_shopping_workflow(self):
        products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
        self.home_page.add_multiple_products_to_cart(products)
        self.home_page.verify_cart_badge_count(len(products))

        self.home_page.click_shopping_cart()
        self.cart_page.verify_cart_page_loaded()

        cart_items = self.cart_page.get_cart_item_names()
        for product in products:
            assert product in cart_items, f"{product} should be in cart"

        cart_prices = self.cart_page.get_cart_item_prices()
        assert len(cart_prices) == len(products), "All product prices should be displayed"

    @pytest.mark.shopping
    @pytest.mark.slow
    def test_performance_with_all_products(self):
        import time

        start_time = time.time()

        product_names = self.home_page.get_product_names()
        self.home_page.add_multiple_products_to_cart(product_names)

        end_time = time.time()
        execution_time = end_time - start_time

        self.home_page.verify_cart_badge_count(len(product_names))
        print(f"Added {len(product_names)} products in {execution_time:.2f} seconds")
        assert execution_time < 30, f"Adding all products took too long: {execution_time:.2f} seconds"

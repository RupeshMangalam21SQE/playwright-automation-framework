"""
Cart Page Object for SauceDemo application
"""

from typing import List
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.config import Config


class CartPage(BasePage):
    """Cart page object for SauceDemo"""

    def __init__(self, page: Page):
        super().__init__(page)

    # Page URL and Title
    def get_page_url(self) -> str:
        return f"{Config.get_base_url()}cart.html"

    def get_page_title(self) -> str:
        return "Swag Labs"

    # Locators
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    CART_ITEM_PRICE = ".inventory_item_price"
    REMOVE_BUTTON = "[data-test*='remove']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CART_CONTAINER = "#cart_contents_container"

    def verify_cart_page_loaded(self) -> None:
        """Verify that cart page has loaded correctly"""
        assert self.is_element_visible(self.CART_CONTAINER), "Cart container is not visible"
        assert self.is_element_visible(self.CHECKOUT_BUTTON), "Checkout button is not visible"

    def get_cart_item_count(self) -> int:
        """Get total number of items in cart"""
        return self.get_element_count(self.CART_ITEM)

    def get_cart_item_names(self) -> List[str]:
        """Get names of all items in cart"""
        return self.get_all_text_contents(self.CART_ITEM_NAME)

    def get_cart_item_prices(self) -> List[str]:
        """Get prices of all items in cart"""
        return self.get_all_text_contents(self.CART_ITEM_PRICE)

    def remove_item_by_name(self, product_name: str) -> None:
        """Remove a specific product from cart by name"""
        button_locator = f"{self.CART_ITEM}:has-text('{product_name}') {self.REMOVE_BUTTON}"
        if self.is_element_visible(button_locator):
            self.click_element(button_locator)

    def continue_shopping(self) -> None:
        """Click continue shopping button"""
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)

    def checkout(self) -> None:
        """Click checkout button"""
        self.click_element(self.CHECKOUT_BUTTON)

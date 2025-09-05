from typing import Dict, List
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage
from utils.config import Config
import time


class HomePage(BasePage):
    """Home/Inventory page object for SauceDemo"""

    # ---------------- Page URL & Title ----------------
    def get_page_url(self) -> str:
        return f"{Config.get_base_url()}inventory.html"

    def get_page_title(self) -> str:
        return "Swag Labs"

    # ---------------- Locators ----------------
    HEADER_CONTAINER = ".header_container"
    APP_LOGO = ".app_logo"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    BURGER_MENU = "#react-burger-menu-btn"
    CLOSE_MENU = "#react-burger-cross-btn"
    SIDEBAR_MENU = ".bm-menu"
    LOGOUT_LINK = "#logout_sidebar_link"
    RESET_APP_LINK = "#reset_sidebar_link"
    INVENTORY_CONTAINER = "#inventory_container"
    INVENTORY_ITEM = ".inventory_item"
    INVENTORY_ITEM_NAME = ".inventory_item_name"
    INVENTORY_ITEM_PRICE = ".inventory_item_price"
    ADD_TO_CART_BUTTON = "[data-test*='add-to-cart']"
    REMOVE_BUTTON = "[data-test*='remove']"

    SORT_NAME_ASC = "az"
    SORT_NAME_DESC = "za"

    # ---------------- Methods ----------------
    def verify_home_page_loaded(self) -> None:
        """Verify that home page has loaded correctly"""
        self.verify_current_url()
        assert self.wait_for_element(self.APP_LOGO, timeout=5000), "App logo not visible"
        assert self.wait_for_element(self.INVENTORY_CONTAINER, timeout=5000), "Inventory container not visible"
        assert self.wait_for_element(self.SHOPPING_CART_LINK, timeout=5000), "Shopping cart link not visible"

    def add_product_to_cart_by_name(self, product_name: str) -> None:
        """Add product to cart by name with retries"""
        button_name = product_name.lower().replace(" ", "-")
        locator = f"[data-test='add-to-cart-{button_name}']"
        retries = 3
        for _ in range(retries):
            try:
                self.click_element(locator, timeout=3000)
                return
            except PlaywrightTimeoutError:
                time.sleep(1)
        raise Exception(f"Failed to add {product_name} to cart")

    def is_product_in_cart(self, product_name: str) -> bool:
        """Check if product is already added to cart"""
        button_name = product_name.lower().replace(" ", "-")
        locator = f"[data-test='remove-{button_name}']"
        return self.is_element_visible(locator, timeout=2000)

    def get_product_names(self) -> List[str]:
        """Get all product names with explicit wait"""
        self.wait_for_element(self.INVENTORY_CONTAINER, timeout=5000)
        return self.get_all_text_contents(self.INVENTORY_ITEM_NAME)

    def sort_products(self, sort_option: str) -> None:
        """Sort products with retry"""
        retries = 2
        for _ in range(retries):
            try:
                self.select_dropdown_option(self.PRODUCT_SORT_DROPDOWN, sort_option, by="value")
                return
            except PlaywrightTimeoutError:
                time.sleep(1)
        raise Exception(f"Failed to sort products by {sort_option}")

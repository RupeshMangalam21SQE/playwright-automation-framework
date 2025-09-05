from typing import Dict
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage
import time


class ProductPage(BasePage):
    """Product detail page object for SauceDemo"""

    # ---------------- Page URL & Title ----------------
    def get_page_url(self) -> str:
        return f"{self.get_base_url()}inventory-item.html"

    def get_page_title(self) -> str:
        return "Swag Labs"

    # ---------------- Locators ----------------
    BACK_TO_PRODUCTS = "[data-test='back-to-products']"
    PRODUCT_IMAGE = ".inventory_details_img"
    PRODUCT_NAME = "[data-test='inventory-item-name']"
    PRODUCT_DESCRIPTION = "[data-test='inventory-item-desc']"
    PRODUCT_PRICE = "[data-test='inventory-item-price']"
    ADD_TO_CART_BUTTON = "[data-test*='add-to-cart']"
    REMOVE_BUTTON = "[data-test*='remove']"

    # ---------------- Methods ----------------
    def verify_product_page_loaded(self) -> None:
        """Verify that product page has loaded correctly"""
        assert self.wait_for_element(self.PRODUCT_NAME, timeout=5000), "Product name not visible"
        assert self.wait_for_element(self.PRODUCT_IMAGE, timeout=5000), "Product image not visible"
        assert self.wait_for_element(self.PRODUCT_PRICE, timeout=5000), "Product price not visible"
        assert self.wait_for_element(self.BACK_TO_PRODUCTS, timeout=5000), "Back to products button not visible"

    def get_product_details(self) -> Dict[str, str]:
        """Get all product details with explicit waits"""
        self.wait_for_element(self.PRODUCT_NAME, timeout=5000)
        return {
            "name": self.get_text(self.PRODUCT_NAME),
            "description": self.get_text(self.PRODUCT_DESCRIPTION),
            "price": self.get_text(self.PRODUCT_PRICE),
        }

    def add_to_cart(self) -> None:
        """Add product to cart with retry"""
        retries = 3
        for _ in range(retries):
            try:
                if self.is_element_visible(self.ADD_TO_CART_BUTTON, timeout=3000):
                    self.click_element(self.ADD_TO_CART_BUTTON)
                    return
            except PlaywrightTimeoutError:
                time.sleep(1)
        raise Exception("Failed to add product to cart")

    def remove_from_cart(self) -> None:
        """Remove product from cart with retry"""
        retries = 3
        for _ in range(retries):
            try:
                if self.is_element_visible(self.REMOVE_BUTTON, timeout=3000):
                    self.click_element(self.REMOVE_BUTTON)
                    return
            except PlaywrightTimeoutError:
                time.sleep(1)
        raise Exception("Failed to remove product from cart")

    def back_to_products(self) -> None:
        """Navigate back to products page with wait"""
        self.wait_for_element(self.BACK_TO_PRODUCTS, timeout=3000)
        self.click_element(self.BACK_TO_PRODUCTS)

    def is_product_in_cart(self) -> bool:
        """Check if product is in cart"""
        return self.is_element_visible(self.REMOVE_BUTTON, timeout=2000)

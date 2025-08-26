"""
Product Detail Page Object for SauceDemo application
"""

from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.config import Config
from typing import Dict


class ProductPage(BasePage):
    """Product detail page object for SauceDemo"""
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def get_page_url(self) -> str:
        return f"{Config.get_base_url()}inventory-item.html"
    
    def get_page_title(self) -> str:
        return "Swag Labs"
    
    # Locators
    BACK_TO_PRODUCTS = "[data-test='back-to-products']"
    PRODUCT_IMAGE = ".inventory_details_img"
    PRODUCT_NAME = "[data-test='inventory-item-name']"
    PRODUCT_DESCRIPTION = "[data-test='inventory-item-desc']"
    PRODUCT_PRICE = "[data-test='inventory-item-price']"
    ADD_TO_CART_BUTTON = "[data-test*='add-to-cart']"
    REMOVE_BUTTON = "[data-test*='remove']"
    
    def verify_product_page_loaded(self) -> None:
        """Verify that product page has loaded correctly"""
        assert self.is_element_visible(self.PRODUCT_NAME), "Product name is not visible"
        assert self.is_element_visible(self.PRODUCT_IMAGE), "Product image is not visible"
        assert self.is_element_visible(self.PRODUCT_PRICE), "Product price is not visible"
        assert self.is_element_visible(self.BACK_TO_PRODUCTS), "Back to products button is not visible"
    
    def get_product_details(self) -> Dict[str, str]:
        """Get all product details"""
        return {
            "name": self.get_text(self.PRODUCT_NAME),
            "description": self.get_text(self.PRODUCT_DESCRIPTION),
            "price": self.get_text(self.PRODUCT_PRICE),
        }
    
    def add_to_cart(self) -> None:
        """Add product to cart"""
        if self.is_element_visible(self.ADD_TO_CART_BUTTON):
            self.click_element(self.ADD_TO_CART_BUTTON)
    
    def remove_from_cart(self) -> None:
        """Remove product from cart"""
        if self.is_element_visible(self.REMOVE_BUTTON):
            self.click_element(self.REMOVE_BUTTON)
    
    def back_to_products(self) -> None:
        """Navigate back to products page"""
        self.click_element(self.BACK_TO_PRODUCTS)
    
    def is_product_in_cart(self) -> bool:
        """Check if product is in cart"""
        return self.is_element_visible(self.REMOVE_BUTTON)

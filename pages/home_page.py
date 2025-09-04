"""
Home/Inventory Page Object for SauceDemo application
"""

from typing import Dict, List

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.config import Config


class HomePage(BasePage):
    """Home/Inventory page object for SauceDemo"""

    def __init__(self, page: Page):
        super().__init__(page)

    # Page URL and Title
    def get_page_url(self) -> str:
        return f"{Config.get_base_url()}inventory.html"

    def get_page_title(self) -> str:
        return "Swag Labs"

    # Header Locators
    HEADER_CONTAINER = ".header_container"
    APP_LOGO = ".app_logo"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    BURGER_MENU = "#react-burger-menu-btn"

    # Burger Menu Items
    SIDEBAR_MENU = ".bm-menu"
    ALL_ITEMS_LINK = "#inventory_sidebar_link"
    ABOUT_LINK = "#about_sidebar_link"
    LOGOUT_LINK = "#logout_sidebar_link"
    RESET_APP_LINK = "#reset_sidebar_link"
    CLOSE_MENU = "#react-burger-cross-btn"

    # Sort and Filter
    PRODUCT_SORT_DROPDOWN = "[data-test='product_sort_container']"

    # Product Grid
    INVENTORY_CONTAINER = "#inventory_container"
    INVENTORY_LIST = ".inventory_list"
    INVENTORY_ITEM = ".inventory_item"
    INVENTORY_ITEM_NAME = ".inventory_item_name"
    INVENTORY_ITEM_PRICE = ".inventory_item_price"
    INVENTORY_ITEM_DESC = ".inventory_item_desc"
    INVENTORY_ITEM_IMG = ".inventory_item_img"

    # Add to Cart Buttons
    ADD_TO_CART_BUTTON = "[data-test*='add-to-cart']"
    REMOVE_BUTTON = "[data-test*='remove']"

    # Footer
    FOOTER = ".footer"
    FOOTER_TEXT = ".footer_copy"

    # Sort Options
    SORT_NAME_ASC = "az"
    SORT_NAME_DESC = "za"
    SORT_PRICE_LOW_HIGH = "lohi"
    SORT_PRICE_HIGH_LOW = "hilo"

    def verify_home_page_loaded(self) -> None:
        """Verify that home page has loaded correctly"""
        self.verify_current_url()
        assert self.is_element_visible(self.APP_LOGO), "App logo is not visible"
        assert self.is_element_visible(
            self.INVENTORY_CONTAINER
        ), "Inventory container is not visible"
        assert self.is_element_visible(
            self.SHOPPING_CART_LINK
        ), "Shopping cart link is not visible"

    def get_page_title_text(self) -> str:
        """Get the page title text from the logo"""
        return self.get_text(self.APP_LOGO)

    def open_burger_menu(self) -> None:
        """Open the burger menu"""
        self.click_element(self.BURGER_MENU)
        self.wait_for_element(self.SIDEBAR_MENU, "visible")

    def close_burger_menu(self) -> None:
        """Close the burger menu"""
        if self.is_element_visible(self.CLOSE_MENU):
            self.click_element(self.CLOSE_MENU)

    def logout(self) -> None:
        """Logout from the application"""
        self.open_burger_menu()
        self.click_element(self.LOGOUT_LINK)

    def reset_app_state(self) -> None:
        """Reset application state"""
        self.open_burger_menu()
        self.click_element(self.RESET_APP_LINK)
        self.close_burger_menu()

    def get_cart_item_count(self) -> int:
        """Get the number of items in cart"""
        if self.is_element_visible(self.SHOPPING_CART_BADGE):
            badge_text = self.get_text(self.SHOPPING_CART_BADGE)
            return int(badge_text) if badge_text.isdigit() else 0
        return 0

    def click_shopping_cart(self) -> None:
        """Click on shopping cart icon"""
        self.click_element(self.SHOPPING_CART_LINK)

    def sort_products(self, sort_option: str) -> None:
        """Sort products by given option"""
        self.select_dropdown_option(self.PRODUCT_SORT_DROPDOWN, sort_option, by="value")

    def get_product_count(self) -> int:
        """Get total number of products displayed"""
        return self.get_element_count(self.INVENTORY_ITEM)

    def get_product_names(self) -> List[str]:
        """Get list of all product names"""
        return self.get_all_text_contents(self.INVENTORY_ITEM_NAME)

    def get_product_prices(self) -> List[str]:
        """Get list of all product prices"""
        return self.get_all_text_contents(self.INVENTORY_ITEM_PRICE)

    def get_product_info(self, product_index: int = 0) -> Dict[str, str]:
        """Get information about a specific product"""
        products = self.page.locator(self.INVENTORY_ITEM)
        if product_index >= products.count():
            raise IndexError(f"Product index {product_index} is out of range")

        product = products.nth(product_index)
        return {
            "name": product.locator(self.INVENTORY_ITEM_NAME).text_content() or "",
            "price": product.locator(self.INVENTORY_ITEM_PRICE).text_content() or "",
            "description": product.locator(self.INVENTORY_ITEM_DESC).text_content()
            or "",
        }

    def click_product_name(self, product_name: str) -> None:
        """Click on a product name to view details"""
        product_locator = f"{self.INVENTORY_ITEM_NAME}:has-text('{product_name}')"
        self.click_element(product_locator)

    def add_product_to_cart_by_name(self, product_name: str) -> None:
        """Add product to cart by product name"""
        # Convert product name to button data-test attribute format
        button_name = product_name.lower().replace(" ", "-")
        button_locator = f"[data-test='add-to-cart-{button_name}']"
        self.click_element(button_locator)

    def remove_product_from_cart_by_name(self, product_name: str) -> None:
        """Remove product from cart by product name"""
        button_name = product_name.lower().replace(" ", "-")
        button_locator = f"[data-test='remove-{button_name}']"
        self.click_element(button_locator)

    def add_product_to_cart_by_index(self, product_index: int) -> None:
        """Add product to cart by index position"""
        products = self.page.locator(self.INVENTORY_ITEM)
        if product_index >= products.count():
            raise IndexError(f"Product index {product_index} is out of range")

        add_button = products.nth(product_index).locator(self.ADD_TO_CART_BUTTON)
        add_button.click()

    def is_product_in_cart(self, product_name: str) -> bool:
        """Check if product is already added to cart"""
        button_name = product_name.lower().replace(" ", "-")
        remove_button_locator = f"[data-test='remove-{button_name}']"
        return self.is_element_visible(remove_button_locator, timeout=1000)

    def verify_products_sorted_by_name_asc(self) -> None:
        """Verify products are sorted by name A-Z"""
        product_names = self.get_product_names()
        sorted_names = sorted(product_names)
        assert (
            product_names == sorted_names
        ), f"Products not sorted A-Z: {product_names}"

    def verify_products_sorted_by_name_desc(self) -> None:
        """Verify products are sorted by name Z-A"""
        product_names = self.get_product_names()
        sorted_names = sorted(product_names, reverse=True)
        assert (
            product_names == sorted_names
        ), f"Products not sorted Z-A: {product_names}"

    def add_multiple_products_to_cart(self, product_names: List[str]) -> None:
        """Add multiple products to cart"""
        for product_name in product_names:
            self.add_product_to_cart_by_name(product_name)

    def verify_cart_badge_count(self, expected_count: int) -> None:
        """Verify the cart badge shows expected count"""
        actual_count = self.get_cart_item_count()
        assert (
            actual_count == expected_count
        ), f"Expected cart count {expected_count}, but got {actual_count}"

"""
Test data management for the Playwright automation framework
"""

from typing import Dict, List, Any
import os
import json
import csv


class LoginTestData:
    """Login test data provider"""
    
    VALID_USERS = [
        {"username": "standard_user", "password": "secret_sauce", "type": "standard"},
        {"username": "problem_user", "password": "secret_sauce", "type": "problem"},
        {"username": "performance_glitch_user", "password": "secret_sauce", "type": "performance"},
    ]
    
    INVALID_USERS = [
        {"username": "locked_out_user", "password": "secret_sauce", "error": "locked_out"},
        {"username": "invalid_user", "password": "secret_sauce", "error": "invalid_credentials"},
        {"username": "standard_user", "password": "wrong_password", "error": "invalid_credentials"},
        {"username": "", "password": "secret_sauce", "error": "username_required"},
        {"username": "standard_user", "password": "", "error": "password_required"},
    ]
    
    @classmethod
    def get_valid_user(cls, user_type: str = "standard") -> Dict[str, str]:
        """Get valid user by type"""
        for user in cls.VALID_USERS:
            if user["type"] == user_type:
                return user
        return cls.VALID_USERS[0]  # Return standard user if type not found
    
    @classmethod
    def get_invalid_user(cls, error_type: str) -> Dict[str, str]:
        """Get invalid user by error type"""
        for user in cls.INVALID_USERS:
            if user["error"] == error_type:
                return user
        return cls.INVALID_USERS[0]  # Return first invalid user if type not found


class ProductTestData:
    """Product test data provider"""
    
    PRODUCTS = [
        {
            "name": "Sauce Labs Backpack",
            "price": "$29.99",
            "id": "sauce-labs-backpack",
            "description": "carry.allTheThings() with the sleek, streamlined Sly Pack"
        },
        {
            "name": "Sauce Labs Bike Light", 
            "price": "$9.99",
            "id": "sauce-labs-bike-light",
            "description": "A red light isn't the desired state in testing"
        },
        {
            "name": "Sauce Labs Bolt T-Shirt",
            "price": "$15.99", 
            "id": "sauce-labs-bolt-t-shirt",
            "description": "Get your testing superhero on with the Sauce Labs bolt T-shirt"
        }
    ]
    
    @classmethod
    def get_product_by_name(cls, name: str) -> Dict[str, str]:
        """Get product by name"""
        for product in cls.PRODUCTS:
            if product["name"] == name:
                return product
        return cls.PRODUCTS[0]  # Return first product if name not found
    
    @classmethod
    def get_cheapest_product(cls) -> Dict[str, str]:
        """Get the cheapest product"""
        return min(cls.PRODUCTS, key=lambda x: float(x["price"].replace("$", "")))
    
    @classmethod
    def get_most_expensive_product(cls) -> Dict[str, str]:
        """Get the most expensive product"""
        return max(cls.PRODUCTS, key=lambda x: float(x["price"].replace("$", "")))


class CheckoutTestData:
    """Checkout form test data provider"""
    
    VALID_CHECKOUT_INFO = {
        "first_name": "John",
        "last_name": "Doe", 
        "postal_code": "12345"
    }
    
    INVALID_CHECKOUT_DATA = [
        {"first_name": "", "last_name": "Doe", "postal_code": "12345", "error": "first_name_required"},
        {"first_name": "John", "last_name": "", "postal_code": "12345", "error": "last_name_required"},
        {"first_name": "John", "last_name": "Doe", "postal_code": "", "error": "postal_code_required"},
    ]
    
    @classmethod
    def get_valid_checkout_info(cls) -> Dict[str, str]:
        """Get valid checkout information"""
        return cls.VALID_CHECKOUT_INFO.copy()
    
    @classmethod
    def get_invalid_checkout_info(cls, error_type: str) -> Dict[str, str]:
        """Get invalid checkout information by error type"""
        for data in cls.INVALID_CHECKOUT_DATA:
            if data["error"] == error_type:
                return {k: v for k, v in data.items() if k != "error"}
        return cls.INVALID_CHECKOUT_DATA[0]

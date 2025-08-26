"""
Helper utilities for the Playwright automation framework
"""

import json
import csv
import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from playwright.sync_api import Page
from faker import Faker
import pandas as pd
from utils.config import Config
import requests



class TestDataManager:
    """Manages test data from various sources"""
    
    def __init__(self):
        self.faker = Faker()
        self.data_dir = Config.TEST_DATA_DIR
        os.makedirs(self.data_dir, exist_ok=True)
    
    def get_login_test_cases(self) -> List[Dict[str, str]]:
        """Get login test cases from CSV or generate default ones"""
        csv_file = os.path.join(self.data_dir, "login_test_data.csv")
        
        if os.path.exists(csv_file):
            return self._read_csv_data(csv_file)
        else:
            return self._get_default_login_data()
    
    def _read_csv_data(self, file_path: str) -> List[Dict[str, str]]:
        """Read test data from CSV file"""
        try:
            df = pd.read_csv(file_path)
            return df.to_dict('records')
        except Exception as e:
            logging.error(f"Error reading CSV file {file_path}: {e}")
            return self._get_default_login_data()
    
    def _get_default_login_data(self) -> List[Dict[str, str]]:
        """Get default login test data"""
        return [
            {"username": "standard_user", "password": "secret_sauce", "expected_result": "success"},
            {"username": "locked_out_user", "password": "secret_sauce", "expected_result": "locked_out"},
            {"username": "problem_user", "password": "secret_sauce", "expected_result": "success"},
            {"username": "performance_glitch_user", "password": "secret_sauce", "expected_result": "success"},
            {"username": "invalid_user", "password": "secret_sauce", "expected_result": "invalid_credentials"},
            {"username": "standard_user", "password": "wrong_password", "expected_result": "invalid_credentials"},
            {"username": "", "password": "secret_sauce", "expected_result": "username_required"},
            {"username": "standard_user", "password": "", "expected_result": "password_required"},
        ]
    
    def generate_fake_user_data(self) -> Dict[str, str]:
        """Generate fake user data for testing"""
        return {
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "email": self.faker.email(),
            "phone": self.faker.phone_number(),
            "address": self.faker.address(),
            "company": self.faker.company(),
            "username": self.faker.user_name(),
            "password": self.faker.password(length=12, special_chars=True),
        }


class ScreenshotHelper:
    """Helper class for taking and managing screenshots"""
    
    def __init__(self, page: Page):
        self.page = page
        self.screenshot_dir = Config.SCREENSHOTS_DIR
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def take_screenshot(self, name: str = None, full_page: bool = True) -> str:
        """Take a screenshot with optional name"""
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}"
        
        if not name.endswith('.png'):
            name += '.png'
        
        screenshot_path = os.path.join(self.screenshot_dir, name)
        self.page.screenshot(path=screenshot_path, full_page=full_page)
        logging.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path


class APIHelper:
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.session = requests.Session()

    def _abs_url(self, endpoint):
        # Accept both '/posts' and 'posts'
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        return self.base_url + endpoint

    def get(self, endpoint, **kwargs):
        resp = self.session.get(self._abs_url(endpoint), **kwargs)
        return self._resp_data(resp)

    def post(self, endpoint, json=None, **kwargs):
        resp = self.session.post(self._abs_url(endpoint), json=json, **kwargs)
        return self._resp_data(resp)

    def put(self, endpoint, json=None, **kwargs):
        resp = self.session.put(self._abs_url(endpoint), json=json, **kwargs)
        return self._resp_data(resp)

    def delete(self, endpoint, **kwargs):
        resp = self.session.delete(self._abs_url(endpoint), **kwargs)
        return self._resp_data(resp)

    def _resp_data(self, resp):
        try:
            data = resp.json()
        except Exception:
            data = resp.text
        return {
            "status_code": resp.status_code,
            "ok": resp.ok,
            "json": data,
            "headers": dict(resp.headers),
        }

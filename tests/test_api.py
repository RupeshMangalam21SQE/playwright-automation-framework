"""
API Testing combined with UI validation
"""

import pytest
from playwright.sync_api import Page
from utils.helpers import APIHelper
from pages.login_page import LoginPage


class TestAPIIntegration:
    """API testing combined with UI validation"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test"""
        self.api_helper = APIHelper()
        self.login_page = LoginPage(page)
    
    @pytest.mark.api
    def test_api_user_creation(self):
        """Test API user creation"""
        # Arrange
        user_data = {
            "name": "Test User",
            "job": "QA Engineer"
        }
        
        # Act
        response = self.api_helper.post("/users", json_data=user_data)
        
        # Assert
        assert response["ok"], f"API request failed: {response}"
        assert response["status_code"] == 201, f"Expected 201, got {response['status_code']}"
        
        response_data = response["json"]
        assert response_data["name"] == user_data["name"], "Name should match"
        assert response_data["job"] == user_data["job"], "Job should match"
        assert "id" in response_data, "Response should contain ID"
        assert "createdAt" in response_data, "Response should contain creation timestamp"
    
    @pytest.mark.api
    def test_api_get_users(self):
        """Test API get users endpoint"""
        # Act
        response = self.api_helper.get("/users?page=2")
        
        # Assert
        assert response["ok"], f"API request failed: {response}"
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        response_data = response["json"]
        assert "data" in response_data, "Response should contain data"
        assert "page" in response_data, "Response should contain page info"
        assert response_data["page"] == 2, "Should be page 2"
        assert len(response_data["data"]) > 0, "Should contain user data"
    
    @pytest.mark.api
    def test_api_user_update(self):
        """Test API user update"""
        # Arrange
        user_id = 2
        update_data = {
            "name": "Updated Name",
            "job": "Senior QA Engineer"
        }
        
        # Act
        response = self.api_helper.put(f"/users/{user_id}", json_data=update_data)
        
        # Assert
        assert response["ok"], f"API request failed: {response}"
        assert response["status_code"] == 200, f"Expected 200, got {response['status_code']}"
        
        response_data = response["json"]
        assert response_data["name"] == update_data["name"], "Name should be updated"
        assert response_data["job"] == update_data["job"], "Job should be updated"
        assert "updatedAt" in response_data, "Response should contain update timestamp"
    
    @pytest.mark.api
    def test_api_user_deletion(self):
        """Test API user deletion"""
        # Arrange
        user_id = 2
        
        # Act
        response = self.api_helper.delete(f"/users/{user_id}")
        
        # Assert
        assert response["ok"], f"API request failed: {response}"
        assert response["status_code"] == 204, f"Expected 204, got {response['status_code']}"
    
    @pytest.mark.api
    @pytest.mark.ui
    def test_api_and_ui_integration(self):
        """Test combining API calls with UI validation"""
        # API: Get user data
        api_response = self.api_helper.get("/users/2")
        assert api_response["ok"], "API request should succeed"
        
        user_data = api_response["json"]["data"]
        user_email = user_data["email"]
        
        # UI: Navigate to login page and verify it loads
        self.login_page.navigate_to_login()
        self.login_page.verify_login_page_loaded()
        
        # UI: Use API data in UI context (example: fill email field if it existed)
        # This is a conceptual example since SauceDemo doesn't have email field
        # In real scenarios, you might populate forms with API-generated data
        
        # Log the integration
        print(f"Successfully integrated API data: {user_email} with UI testing")
        
        # Verify UI still works after API calls
        self.login_page.login_with_standard_user()
        self.login_page.verify_successful_login()
    
    @pytest.mark.api
    def test_api_error_handling(self):
        """Test API error handling"""
        # Test invalid endpoint
        response = self.api_helper.get("/invalid-endpoint")
        assert not response["ok"], "Request to invalid endpoint should fail"
        assert response["status_code"] == 404, "Should return 404 for invalid endpoint"
    
    @pytest.mark.api
    def test_api_performance(self):
        """Test API performance"""
        import time
        
        start_time = time.time()
        
        # Make multiple API calls
        for i in range(5):
            response = self.api_helper.get(f"/users?page={i+1}")
            assert response["ok"], f"Request {i+1} should succeed"
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Assert performance
        assert total_time < 10, f"5 API calls took too long: {total_time:.2f} seconds"
        print(f"5 API calls completed in {total_time:.2f} seconds")
    
    @pytest.mark.api
    def test_api_data_validation(self):
        """Test API response data validation"""
        response = self.api_helper.get("/users/1")
        
        assert response["ok"], "API request should succeed"
        user_data = response["json"]["data"]
        
        # Validate data structure
        required_fields = ["id", "email", "first_name", "last_name", "avatar"]
        for field in required_fields:
            assert field in user_data, f"Required field '{field}' missing from response"
        
        # Validate data types
        assert isinstance(user_data["id"], int), "ID should be an integer"
        assert isinstance(user_data["email"], str), "Email should be a string"
        assert "@" in user_data["email"], "Email should contain @ symbol"
        
        # Validate data format
        assert user_data["avatar"].startswith("https://"), "Avatar should be HTTPS URL"

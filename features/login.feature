Feature: User Login
  As a user of the application
  I want to be able to log in with my credentials
  So that I can access the application features

  Background:
    Given I am on the login page

  @smoke @login
  Scenario: Successful login with valid credentials
    When I enter valid credentials
    Then I should be redirected to the home page
    And I should see the product inventory

  @smoke @login  
  Scenario: Login with invalid username
    When I enter an invalid username and valid password
    Then I should see an error message "Username and password do not match any user"
    And I should remain on the login page

  @smoke @login
  Scenario: Login with invalid password
    When I enter a valid username and invalid password  
    Then I should see an error message "Username and password do not match any user"
    And I should remain on the login page

  @login
  Scenario: Login with locked out user
    When I enter locked out user credentials
    Then I should see an error message "Sorry, this user has been locked out"
    And I should remain on the login page

  @login
  Scenario: Login with empty credentials
    When I click the login button without entering credentials
    Then I should see an error message "Username is required"
    And I should remain on the login page

  @login @regression
  Scenario Outline: Login with different user types
    When I login with "<username>" and "<password>"
    Then the login result should be "<result>"

    Examples:
      | username                | password     | result            |
      | standard_user          | secret_sauce | success           |
      | locked_out_user        | secret_sauce | locked_out        |
      | problem_user           | secret_sauce | success           |
      | performance_glitch_user| secret_sauce | success           |
      | invalid_user           | secret_sauce | invalid_credentials|
      | standard_user          | wrong_pass   | invalid_credentials|

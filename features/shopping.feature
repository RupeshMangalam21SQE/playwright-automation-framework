Feature: Shopping Cart Management
  As a customer
  I want to manage items in my shopping cart
  So that I can purchase the products I need

  Background:
    Given I am logged in as a standard user
    And I am on the home page

  @smoke @shopping
  Scenario: Add single product to cart
    When I add "Sauce Labs Backpack" to the cart
    Then the product should be in the cart
    And the cart badge should show "1"

  @shopping
  Scenario: Add multiple products to cart
    When I add the following products to the cart:
      | Sauce Labs Backpack    |
      | Sauce Labs Bike Light  |
      | Sauce Labs Bolt T-Shirt|
    Then all products should be in the cart
    And the cart badge should show "3"

  @shopping
  Scenario: Remove product from cart
    Given I have "Sauce Labs Backpack" in the cart
    When I remove "Sauce Labs Backpack" from the cart
    Then the product should not be in the cart
    And the cart badge should show "0"

  @shopping
  Scenario: Sort products by name
    When I sort products by "Name (A to Z)"
    Then products should be sorted alphabetically ascending
    When I sort products by "Name (Z to A)"
    Then products should be sorted alphabetically descending

  @regression @shopping
  Scenario: Complete shopping workflow
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    And I click on the shopping cart
    Then I should be on the cart page
    And I should see 2 items in the cart

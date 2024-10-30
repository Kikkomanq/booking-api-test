Feature: Check if happy path for e2e booking is working 
    As an API consumer
    I want to test that happy path for E2E booking is working 
    So that I can verify booking flow is working

  @regression   @v3.4.0
  Scenario: Retrieve the list of available tours
    Given I set GET method for tours endpoint
    When I send GET HTTP request
    Then the search response status should be 200
    And There should be available tours for booking 

  @regression  @v3.5.0
  Scenario: Retrieve details and optional services of first selected tour
    Given I get the results of tours endpoint
    When I get the tour ID and Option ID
    And I send tour ID and Option ID
    Then ShoppingCartReference is generated

  @regression  @v3.5.0
  Scenario: Verify that cart reference id is generated
    Given optionalServices and ShoppingCartReference is generated
    When  I send booking refereference to cart endpoint
    Then  Id with booking cart will be generated
    
  @regression @v3.4.0
  Scenario: Verify that /check endpoint is working and that tour is bookable
    Given Cart Id is present 
    When I send cart Id to check endpoint
    Then Selected Tour should be available for booking with message "Item bookable"

  @regression 
  Scenario: Verify that reservation can be done with valid booking reference
    Given Cart Id is present
    When I send cart Id to reserve endpoint
    Then Selected Tour should be reserved with message "Item reserved"

  @regression
  Scenario: Verify that booking can be done with valid booking reference and valid payload
    Given Cart Id is present
    When I send valid payload so to make booking
    Then A unique booking identifier is returned that can be used for further booking amends

  @regression
  Scenario: Verify that booking CANNOT be done with valid booking reference and invalid payload
    Given Cart Id is present
    When I send invalid payload so to make booking
    Then Booking cant be made because externalIdentifier is already used

  @regression
  Scenario: Verify that get booking endpoint is created and returned booking data
    Given Cart Id is present
    When I send valid payload so to make booking
    Then A unique booking identifier is returned that can be used for further booking amends
    And A booking endpoint returnes valid status code
    And Booking data is returned
    



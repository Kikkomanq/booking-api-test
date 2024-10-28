Feature: Check if happy path for e2e booking is working 
    As an API consumer
    I want to test that happy path for E2E booking is working 
    So that I can verify booking flow is working

  Scenario: Retrieve the list of available tours
    Given I set GET method for tours endpoint
    When I send GET HTTP request
    Then the search response status should be 200
    And There should be available tours for booking 


  Scenario: Retrieve details and optional services of first selected tour
    Given I get the results of tours endpoint
    When I get the tour ID and Option ID
    Then I send tour ID and Option ID
    And optionalServices and ShoppingCartReference is generated

  Scenario: Verify that cart reference id is generated
    Given optionalServices and ShoppingCartReference is generated
    When  I send booking refereference to cart endpoint
    Then  Id with booking cart will be generated

  Scenario: Verify that /check endpoint is working and that tour is bookable
    Given Cart Id is present 
    When I send cart Id to check endpoint
    Then Selected Tour should be available for booking with message "Item bookable"

  Scenario: Verify that reservation can be done with valid booking reference
    Given Cart Id is present
    When I send cart Id to reserve endpoint
    Then Selected Tour should be reserved with message "Item reserved"



    



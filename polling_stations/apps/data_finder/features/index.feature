Feature: Check Postcodes
    Scenario: Check postcode with address picker valid station id
    When I visit site page "/"
    Then I should see "Find your polling station"
    Then I fill in "postcode" with "BB11BB"
    Then I submit the form with id "find-polling-station-form"
    Then I should see "Choose Your Address"
    And I should see option "2 Baz Street, Bar Town" in selector "address"
    Then I select "2 Baz Street, Bar Town" from "address"
    Then I submit the form with id "select-address-form"
    Then The browser's URL should contain "address/05"
    And I should see "Your polling station"
    And I should see "walking/driving directions"
    And No errors were thrown

    Scenario: Check postcode with address picker invalid station id
    When I visit site page "/"
    Then I should see "Find your polling station"
    Then I fill in "postcode" with "BB11BB"
    Then I submit the form with id "find-polling-station-form"
    Then I should see "Choose Your Address"
    And I should see option "3 Baz Street, Bar Town" in selector "address"
    Then I select "3 Baz Street, Bar Town" from "address"
    Then I submit the form with id "select-address-form"
    Then The browser's URL should contain "/address/06/"
    And I should see "Contact Foo Council"
    And No errors were thrown

    Scenario: Check postcode without address picker
    When I visit site page "/"
    Then I should see "Find your polling station"
    Then I fill in "postcode" with "NP205GN"
    Then I submit the form with id "find-polling-station-form"
    Then The browser's URL should contain "/address/10/"
    And I should see "Your polling station"
    And I should see "walking/driving directions"
    And No errors were thrown

    Scenario: Check my address not in list
    When I visit site page "/"
    Then I should see "Find your polling station"
    Then I fill in "postcode" with "BB11BB"
    Then I submit the form with id "find-polling-station-form"
    Then I should see "Choose Your Address"
    Then I select "My address is not in the list" from "address"
    Then I submit the form with id "select-address-form"
    Then I should see "Contact Foo Council"
    And No errors were thrown

    Scenario: Check invalid postcode
    When I visit site page "/postcode/foo"
    Then I should see "This doesn't appear to be a valid postcode."
    And No errors were thrown

    Scenario: Check Northern Ireland
    When I visit site page "/"
    Then I should see "Find your polling station"
    Then I fill in "postcode" with "BT15 3JX"
    Then I submit the form with id "find-polling-station-form"
    Then I should see "The Electoral Office for Northern Ireland"
    And I should see "You will need photographic identification"
    And No errors were thrown

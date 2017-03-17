Feature: Check Postcodes
    Scenario: Check postcode with address picker valid station id
    When I visit site page "/"
    Then I should see "Find your polling station"
    Then I fill in "postcode" with "BB11BB"
    Then I submit the only form
    Then I should see "Choose Your Address / Street"
    And I should see option "2 Baz Street, Bar Town" in selector "address"
    Then I select "2 Baz Street, Bar Town" from "address"
    Then I submit the only form
    Then The browser's URL should contain "/address/4/"
    And I should see "Your polling station"
    And I should see "The polling station for BB11BB is"
    And I should see "Get walking directions"
    And No errors were thrown

    Scenario: Check postcode with address picker invalid station id
    When I visit site page "/"
    Then I should see "Find your polling station"
    Then I fill in "postcode" with "BB11BB"
    Then I submit the only form
    Then I should see "Choose Your Address / Street"
    And I should see option "3 Baz Street, Bar Town" in selector "address"
    Then I select "3 Baz Street, Bar Town" from "address"
    Then I submit the only form
    Then The browser's URL should contain "/address/5/"
    And I should see "Contact Foo Council"
    And I should see "We don't have data for your area."
    And No errors were thrown

    Scenario: Check postcode without address picker
    When I visit site page "/"
    Then I should see "Find your polling station"
    Then I fill in "postcode" with "NP205GN"
    Then I submit the only form
    Then The browser's URL should contain "/postcode/NP205GN/"
    And I should see "Your polling station"
    And I should see "The polling station for NP205GN is"
    And I should see "Get walking directions"
    And No errors were thrown

    Scenario: Check my address not in list
    When I visit site page "/"
    Then I should see "Find your polling station"
    Then I fill in "postcode" with "BB11BB"
    Then I submit the only form
    Then I should see "Choose Your Address / Street"
    Then I click "My address is not in the list"
    Then I should see "Contact Foo Council"
    Then I should see "We don't have data for your area."
    Then I should see "We think everyone should be able to find their polling station online. If you agree, please sign up below."
    Then No errors were thrown

    Scenario: Check Northern Ireland postcode
    When I visit site page "/"
    Then I should see "Find your polling station"
    Then I fill in "postcode" with "BT1 1AA"
    Then I submit the only form
    Then I should see "The Electoral Office of Northern Ireland has its own polling station finder: Find your polling station"
    And No errors were thrown

Feature: Smoke tests

    Scenario: Check api docs
    When I visit site page "/api"
    Then I should see "wheredoivote.co.uk Beta API"
    And No errors were thrown

    Scenario: Check api
    When I visit site page "/api/beta"
    Then I should see "Api Root"
    And No errors were thrown

    Scenario: Check email signup form
    When I visit site page "/email/mailing_list"
    Then I should see "Join our mailing list"
    And No errors were thrown

    Scenario: Check feedback form
    When I visit site page "/feedback"
    Then I should see "Did you find this useful?"
    And No errors were thrown

    Scenario: Check bug report form
    When I visit site page "/report_problem"
    Then I should see "Report a Problem"
    And No errors were thrown

    Scenario: Check embed version
    When I visit site page "/embed"
    Then I should see "Enter your postcode"
    And No errors were thrown

    Scenario: Check Example page
    When I visit site page "/example"
    Then I should see "Your polling station"
    And No errors were thrown

Feature: Check Postcodes
    Scenario: Check Islington
    Given I put in the postcode "N19SN"
    I should be told to vote at "Half Moon Crescent Community Hall"
    And the council's phone number is "020 7527 3110"

    Scenario: Check West Berks
    Given I put in the postcode "RG145LD"
    I should be told to vote at "West Berkshire Council"
    And the council's phone number is "01635 519464"
    Given I put in the postcode "RG141LR"
    I should be told to vote at "The Scout Hut"
    And the council's phone number is "01635 519464"


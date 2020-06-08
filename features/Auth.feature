Feature: Authenticate
  Should Authenticate users based on the authorization token

  Scenario: user provides good authentication
    Given a valid authorization token
    When authenticating
    Then a successful authentication response is returned

  Scenario: user provides bad authentication
    Given an invalid authorization token
    When authenticating
    Then a deny authentication response is returned
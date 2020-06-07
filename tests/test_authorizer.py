from unittest import TestCase
from auth import authorizer


class Test(TestCase):
    def test_valid_auth(self):
        password = 'password'
        event = {'authorizationToken': password, 'methodArn': 'arn'}
        expected_response = Test.__expected_auth_response('user', 'Allow', event['methodArn'])

        response = authorizer.lambda_handler(event, None)

        self.assertEqual(expected_response, response)

    def test_invalid_auth(self):
        password = 'bad password'
        event = {'authorizationToken': password, 'methodArn': 'arn'}
        expected_response = Test.__expected_auth_response(None, 'Deny', event['methodArn'])

        response = authorizer.lambda_handler(event, None)

        self.assertEqual(expected_response, response)

    @staticmethod
    def __expected_auth_response(principal, effect, resource):
        return {
            'principalId': principal,
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Sid': 'FirstStatement',
                        'Action': 'execute-api:Invoke',
                        "Effect": effect,
                        'Resource': resource
                    }
                ]
            }
        }

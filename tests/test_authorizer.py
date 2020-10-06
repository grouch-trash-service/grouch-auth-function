from unittest import TestCase
from unittest.mock import patch, MagicMock

import boto3

from auth import authorizer


class Test(TestCase):
    @patch('boto3.session')
    def test_valid_auth(self, test_session):
        password = 'password'
        Test.__mock_boto3_session(test_session)
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

    @patch('boto3.session')
    def test_get_secret(self, test_session):
        Test.__mock_boto3_session(test_session)

        password = authorizer.get_secret()
        self.assertEqual('password', password)

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

    @staticmethod
    def __mock_boto3_session(test_session):
        client = boto3.client('secretsmanager')
        session = boto3.session.Session()
        client.get_secret_value = MagicMock(return_value={'SecretString': '{"API_KEY": "password"}'})
        session.client = MagicMock(return_value=client)
        test_session.Session = MagicMock(return_value=session)
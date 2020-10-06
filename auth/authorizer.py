"""
authorizer module for invoking lambda function to do authentication
"""

import boto3

SECRET_NAME = "grouch/apiKey"


def lambda_handler(event, context):
    """
    lambda function for authenticating users
    :param event: lambda event that contains the authorization token
    :param context: lambda context
    :return: auth policy denoting whether the user is authenticated or not
    """
    print(event)
    print(context)
    if event['authorizationToken'] == get_secret():
        effect = 'Allow'
        principal = 'user'
    else:
        effect = 'Deny'
        principal = None

    return {
        'principalId': principal,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'FirstStatement',
                    'Action': 'execute-api:Invoke',
                    "Effect": effect,
                    'Resource': event['methodArn']
                }
            ]
        }
    }


def get_secret() -> str:
    """
    gets secret from secretsmanager
    :return:
    """
    session = boto3.session.Session()
    client = session.client('secretsmanager')
    secret_value_response = client.get_secret_value(SecretId=SECRET_NAME)
    return secret_value_response['SecretString']

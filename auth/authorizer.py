def lambda_handler(event, context):
    if event['authorizationToken'] == 'password':
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

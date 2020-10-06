"""
step defs for behave tests
"""
import json
import boto3
import botocore

from behave import use_step_matcher, given, when, then

use_step_matcher("re")


@then("a successful authentication response is returned")
def successful_authentication(context):
    """
    :type context: behave.runner.Context
    """
    payload = context.response['Payload']
    response_body = json.loads(payload._raw_stream.data)
    assert __extract_effect_from_policy_document(response_body) == 'Allow'


@when("authenticating")
def authenticating(context):
    """
    :type context: behave.runner.Context
    """
    env = context.config.userdata.get('local', 'false')
    if env == 'true':
        lambda_client = boto3.client('lambda',
                                 region_name='us-east-1',
                                 endpoint_url='http://127.0.0.1:3001',
                                 use_ssl=False,
                                 verify=False,
                                 config=botocore.client.Config(
                                     signature_version=botocore.UNSIGNED,
                                     read_timeout=600,
                                     retries={'max_attempts': 0}
                                 )
                                 )
    else:
        lambda_client = boto3.client('lambda')
    event = {
        'authorizationToken': context.password,
        'methodArn': 'arn:aws:cucumber-test'
    }
    payload = json.dumps(event).encode('utf-8')
    context.response = lambda_client.invoke(FunctionName='AuthFunction', Payload=payload)


@given("a valid authorization token")
def valid_auth_token(context):
    """
    :type context: behave.runner.Context
    """
    secret_name = "grouch/apiKey"
    session = boto3.session.Session()
    client = session.client('secretsmanager')
    secret_value_response = client.get_secret_value(SecretId=secret_name)
    context.password = secret_value_response['SecretString']


@given("an invalid authorization token")
def invalid_auth_token(context):
    """
    :type context: behave.runner.Context
    """
    context.password = 'bad password'


@then("a deny authentication response is returned")
def deny_auth(context):
    """
    :type context: behave.runner.Context
    """
    payload = context.response['Payload']
    response_body = json.loads(payload._raw_stream.data)
    assert __extract_effect_from_policy_document(response_body) == 'Deny'


def __extract_effect_from_policy_document(response_body):
    return response_body['policyDocument']['Statement'][0]['Effect']

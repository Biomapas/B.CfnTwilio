import json

from b_aws_testing_framework.credentials import Credentials
from botocore.response import StreamingBody

from b_twilio_sdk_layer_test.integration.infrastructure import Infrastructure


def test_RESOURCE_lambda_layer_WITH_deployed_lambda_function_EXPECT_execution_successful():
    """
    Test whether the layer provides necessary functionality.

    :return: No return.
    """
    # Create client for lambda service.
    lambda_client = Credentials().boto_session.client('lambda')

    # Invoke specific lambda function.
    response = lambda_client.invoke(
        FunctionName=Infrastructure.get_output(Infrastructure.LAMBDA_FUNCTION_NAME_KEY),
        InvocationType='RequestResponse'
    )

    # Parse the result.
    payload: StreamingBody = response['Payload']
    data = json.loads(payload.read())

    # Assert that the result is as expected.
    assert data is True, data

from aws_cdk.core import Construct
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack

from b_twilio_sdk_layer_test.integration.infrastructure.testing_function import TestingFunction


class Infrastructure(TestingStack):
    LAMBDA_FUNCTION_NAME_KEY = 'LambdaFunctionName'

    def __init__(self, scope: Construct):
        super().__init__(scope=scope)

        function = TestingFunction(self)

        self.add_output(self.LAMBDA_FUNCTION_NAME_KEY, value=function.function_name)

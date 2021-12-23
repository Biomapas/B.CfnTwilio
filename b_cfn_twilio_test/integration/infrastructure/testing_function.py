from aws_cdk.aws_lambda import Function, Code, Runtime
from aws_cdk.core import Stack
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack

from b_twilio_sdk_layer.layer import Layer


class TestingFunction(Function):
    """
    Function that allows us to test whether correct versions are installed.
    """

    def __init__(self, scope: Stack):
        super().__init__(
            scope=scope,
            id=f'{TestingStack.global_prefix()}TestingFunction',
            code=Code.from_inline(
                'def handler(*args, **kwargs):\n'
                '    try:\n'
                '        import twilio\n'
                '        return True\n'
                '    except ImportError:\n'
                '        return False\n'
            ),
            handler='index.handler',
            runtime=Runtime.PYTHON_3_6,
            layers=[
                Layer(
                    scope=scope,
                    name=f'{TestingStack.global_prefix()}TestingTwilioLayer'
                )
            ]
        )

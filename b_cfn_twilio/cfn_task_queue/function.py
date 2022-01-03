from __future__ import annotations

from functools import lru_cache

from aws_cdk.aws_lambda import Code, SingletonFunction, Runtime
from aws_cdk.core import Stack, Duration

from b_twilio_sdk_layer.layer import Layer as TwilioLayer


class TwilioTaskQueueSingletonFunction(SingletonFunction):
    """
    Custom workspace resource Singleton Lambda function.

    Creates a workspace on stack creation.
    Updates the workspace on workspace name change.
    Deletes the workspace on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            name: str
    ) -> None:
        self.__name = name

        super().__init__(
            scope=scope,
            id=name,
            uuid='4b5bfe56-7cb0-4442-bbec-9ba1ed440927',
            function_name=name,
            code=self.__code(),
            layers=[TwilioLayer(scope, f'TwilioLayerFor{name}')],
            timeout=Duration.minutes(1),
            handler='main.index.handler',
            runtime=Runtime.PYTHON_3_8
        )

    @lru_cache
    def __code(self) -> Code:
        from .source import root
        return Code.from_asset(root)

    @property
    def function_name(self):
        return self.__name

from __future__ import annotations

from functools import lru_cache

from aws_cdk.aws_lambda import Code, SingletonFunction, Runtime
from aws_cdk.core import Stack

from b_twilio_sdk_layer.layer import Layer as TwilioLayer


class TwilioWorkspaceSingletonFunction(SingletonFunction):
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
            uuid='3b8d2b61-f286-4bcb-bfe2-1462ecfdf6fb',
            function_name=name,
            code=self.__code(),
            layers=[TwilioLayer(scope, f'TwilioLayerFor{name}')],
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

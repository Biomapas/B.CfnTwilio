from typing import List

from aws_cdk.core import Stack, CustomResource, RemovalPolicy

from b_cfn_twilio.cfn_activity.function import TwilioActivitySingletonFunction
from b_cfn_twilio.cfn_activity.twilio_activity import TwilioActivity


class TwilioActivityResource(CustomResource):
    """
    Custom resource used for managing a Twilio workspace for a deployment.

    Creates a workspace on stack creation.
    Updates the workspace on workspace name change.
    Deletes the workspace on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            name: str,
            twilio_account_sid: str,
            twilio_auth_token: str,
            twilio_workspace_sid: str,
            activities: List[TwilioActivity]
    ) -> None:
        """

        :param scope: CloudFormation template stack in which this resource will belong.
        :param name: Custom resource name.
        :param twilio_account_sid: Twilio Account SID.
        :param twilio_auth_token: Twilio Auth SID.
        :param twilio_workspace_sid: Twilio Workspace SID.
        :param activities: List of Twilio Activities.
        """

        if len(activities) == 0:
            raise AttributeError('At least one cfn_activity must be provided.')

        default_activities_count = len([activity.default for activity in activities if activity.default])
        if default_activities_count != 1:
            raise AttributeError('Exactly one cfn_activity must be default in a Workspace.')

        if len(activities) != len(set([activity.friendly_name for activity in activities])):
            raise AttributeError('Two activities can not have the same name.')

        self.__activities = {
            f'{self.__parametrize_name(activity.friendly_name)}Activity': {
                'friendly_name': activity.friendly_name,
                'availability': activity.availability,
                'default': activity.default
            } for activity in activities
        }

        activity_function = TwilioActivitySingletonFunction(
            scope=scope,
            name=f'{name}Function'
        )

        super().__init__(
            scope=scope,
            id=f'CustomResource{name}',
            service_token=activity_function.function_arn,
            pascal_case_properties=True,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                **self.__activities,
                'TwilioAccountSid': twilio_account_sid,
                'TwilioAuthToken': twilio_auth_token,
                'TwilioWorkspaceSid': twilio_workspace_sid
            }
        )

    def get_activity_sid(self, friendly_name: str) -> str:
        return self.get_att_string(f'{self.__parametrize_name(friendly_name)}ActivitySid')

    def __parametrize_name(self, friendly_name: str) -> str:
        return friendly_name.replace(' ', '')

from aws_cdk.core import Stack, CustomResource, RemovalPolicy

from b_cfn_twilio.cfn_task_queue.function import TwilioTaskQueueSingletonFunction


class TwilioTaskQueueResource(CustomResource):
    """
    Custom resource used for managing a Twilio task_queue for a deployment.

    Creates a task_queue on stack creation.
    Updates the task_queue on task_queue name change.
    Deletes the task_queue on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            twilio_account_sid: str,
            twilio_auth_token: str,
            twilio_workspace_sid: str,
            task_queue_function: TwilioTaskQueueSingletonFunction,
            task_queue_name: str
    ) -> None:
        """
        Constructor.

        :param scope: CloudFormation template stack in which this resource will belong.
        :param twilio_account_sid: Twilio Account SID.
        :param twilio_auth_token: Twilio Auth SID.
        :param twilio_workspace_sid: SID of the Workspace to create TaskQueue for.
        :param task_queue_function: Resource function.
        :param task_queue_name: Name that will be provided to the created TaskQueue.
        """

        super().__init__(
            scope=scope,
            id=f'CustomResource{task_queue_function.function_name}',
            service_token=task_queue_function.function_arn,
            pascal_case_properties=True,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                'TwilioTaskQueueName': task_queue_name,
                'TwilioAccountSid': twilio_account_sid,
                'TwilioAuthToken': twilio_auth_token,
                'TwilioWorkspaceSid': twilio_workspace_sid
            }
        )

    @property
    def task_queue_sid(self):
        return self.get_att_string('TaskQueueSid')

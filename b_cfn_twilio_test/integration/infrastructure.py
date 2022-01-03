import os

from aws_cdk.core import Construct
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack

from b_cfn_twilio.cfn_activity.resource import TwilioActivityResource
from b_cfn_twilio.cfn_activity.twilio_activity import TwilioActivity
from b_cfn_twilio.cfn_task_queue.resource import TwilioTaskQueueResource
from b_cfn_twilio.cfn_workflow.resource import TwilioWorkflowResource
from b_cfn_twilio.cfn_workspace.resource import TwilioWorkspaceResource


class Infrastructure(TestingStack):
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

    WORKSPACE_SID_KEY = 'WorkspaceSidKey'
    TASK_QUEUE_SID_KEY = 'TaskQueueSidKey'
    WORKFLOW_SID_KEY = 'WorkflowSidKey'
    ACTIVITY_AVAILABLE_SID_KEY = 'ActivityAvailableSidKey'
    ACTIVITY_UNAVAILABLE_SID_KEY = 'ActivityUnavailableSidKey'

    def __init__(self, scope: Construct):
        super().__init__(scope=scope)

        workspace = TwilioWorkspaceResource(
            scope=self,
            name=f'{TestingStack.global_prefix()}TestWorkspaceResource',
            workspace_name=f'{TestingStack.global_prefix()}TestWorkspace',
            twilio_account_sid=self.TWILIO_ACCOUNT_SID,
            twilio_auth_token=self.TWILIO_AUTH_TOKEN,
            events_filter=['task.created', 'task.canceled', 'worker.activity.update']
        )

        task_queue = TwilioTaskQueueResource(
            scope=self,
            name=f'{TestingStack.global_prefix()}TestTaskQueueResource',
            task_queue_name=f'{TestingStack.global_prefix()}TestTaskQueue',
            twilio_account_sid=self.TWILIO_ACCOUNT_SID,
            twilio_auth_token=self.TWILIO_AUTH_TOKEN,
            twilio_workspace_sid=workspace.workspace_sid
        )

        workflow = TwilioWorkflowResource(
            scope=self,
            name=f'{TestingStack.global_prefix()}TestWorkflowResource',
            workflow_name=f'{TestingStack.global_prefix()}TestWorkflow',
            task_queue_sid=task_queue.task_queue_sid,
            twilio_account_sid=self.TWILIO_ACCOUNT_SID,
            twilio_auth_token=self.TWILIO_AUTH_TOKEN,
            twilio_workspace_sid=workspace.workspace_sid
        )

        activities = TwilioActivityResource(
            scope=self,
            name=f'{TestingStack.global_prefix()}TestActivityResource',
            twilio_account_sid=self.TWILIO_ACCOUNT_SID,
            twilio_auth_token=self.TWILIO_AUTH_TOKEN,
            twilio_workspace_sid=workspace.workspace_sid,
            activities=[
                TwilioActivity('Available', True, False),
                TwilioActivity('Unavailable', False, True)
            ],
        )

        self.add_output(self.WORKSPACE_SID_KEY, workspace.workspace_sid)
        self.add_output(self.TASK_QUEUE_SID_KEY, task_queue.task_queue_sid)
        self.add_output(self.WORKFLOW_SID_KEY, workflow.workflow_sid)
        self.add_output(self.ACTIVITY_AVAILABLE_SID_KEY, activities.get_activity_sid('Available'))
        self.add_output(self.ACTIVITY_UNAVAILABLE_SID_KEY, activities.get_activity_sid('Unavailable'))

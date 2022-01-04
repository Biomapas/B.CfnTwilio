from twilio.rest import Client

from b_cfn_twilio_test.integration.infrastructure import Infrastructure


def test_RESOURCE_task_queue_WITH_deployed_custom_resource_EXPECT_task_queue_exist():
    """
    Test whether the custom resource created according Twilio resources and they are reachable and exist.

    :return: No return.
    """

    workspace_sid = Infrastructure.get_output(Infrastructure.WORKSPACE_SID_KEY)
    task_queue_sid = Infrastructure.get_output(Infrastructure.TASK_QUEUE_SID_KEY)

    twilio_client = Client(username=Infrastructure.TWILIO_ACCOUNT_SID, password=Infrastructure.TWILIO_AUTH_TOKEN)

    # Make sure the resource exists.
    task_queue = twilio_client.taskrouter.workspaces(workspace_sid).task_queues(task_queue_sid).fetch()
    assert task_queue, task_queue_sid

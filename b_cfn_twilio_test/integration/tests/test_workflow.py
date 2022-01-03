from twilio.rest import Client

from b_cfn_twilio_test.integration.infrastructure import Infrastructure


def test_RESOURCE_workflow_WITH_deployed_custom_resource_EXPECT_workflow_exist():
    """
    Test whether the custom resource created according Twilio resources and they are reachable and exist.

    :return: No return.
    """

    workspace_sid = Infrastructure.get_output(Infrastructure.WORKSPACE_SID_KEY)
    workflow_sid = Infrastructure.get_output(Infrastructure.WORKFLOW_SID_KEY)

    twilio_client = Client(username=Infrastructure.TWILIO_ACCOUNT_SID, password=Infrastructure.TWILIO_AUTH_TOKEN)

    # Make sure the resource exists.
    workflow = twilio_client.taskrouter.workspaces(workspace_sid).workflows(workflow_sid).fetch()
    assert workflow, workflow

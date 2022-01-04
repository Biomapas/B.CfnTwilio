from twilio.rest import Client

from b_cfn_twilio_test.integration.infrastructure import Infrastructure


def test_RESOURCE_activity_WITH_deployed_custom_resource_EXPECT_activities_exist():
    """
    Test whether the custom resource created according Twilio resources and they are reachable and exist.

    :return: No return.
    """

    available_activity_sid = Infrastructure.get_output(Infrastructure.ACTIVITY_AVAILABLE_SID_KEY)
    unavailable_activity_sid = Infrastructure.get_output(Infrastructure.ACTIVITY_UNAVAILABLE_SID_KEY)
    workspace_sid = Infrastructure.get_output(Infrastructure.WORKSPACE_SID_KEY)

    twilio_client = Client(username=Infrastructure.TWILIO_ACCOUNT_SID, password=Infrastructure.TWILIO_AUTH_TOKEN)

    # Find the according resource.
    available_activity = twilio_client.taskrouter.workspaces(workspace_sid).activities(available_activity_sid).fetch()
    unavailable_activity = twilio_client.taskrouter.workspaces(workspace_sid).activities(unavailable_activity_sid).fetch()

    # Assert if values are correct.
    assert available_activity.available is True, available_activity._properties
    assert unavailable_activity.available is False, available_activity._properties

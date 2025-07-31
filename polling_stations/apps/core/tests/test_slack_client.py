from unittest.mock import Mock, patch
import pytest
import io
from slack_sdk.errors import SlackApiError

from core.slack_client import SlackClient, SlackChannelNotFoundError


@pytest.fixture
def mock_webclient():
    with patch("core.slack_client.WebClient") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.conversations_list.return_value = Mock(
            data={"channels": [{"name": "bots", "id": "C123456"}]}
        )
        yield mock_client


@pytest.fixture
def mock_env_token():
    with patch.dict("os.environ") as mock_env:
        mock_env["SLACK_TOKEN"] = "my-secret-env-token"
        yield


class TestSlackClient:
    def test_param_token(self, mock_webclient):
        client = SlackClient(token="some-test-token")
        assert client.token == "some-test-token"

    def test_env_token(self, mock_webclient, mock_env_token):
        client = SlackClient()
        assert client.token == "my-secret-env-token"

    def test_param_token_priority(self, mock_webclient, mock_env_token):
        client = SlackClient(token="override-token")
        assert client.token == "override-token"

    def test_no_token(self, mock_webclient):
        with pytest.raises(ValueError, match="Slack token not provided"):
            SlackClient(token=None)

    def test_get_channel_id_successful(self, mock_webclient, mock_env_token):
        client = SlackClient()
        channel_id = client.get_channel_id_from_name("bots")
        assert channel_id == "C123456"

    def test_init_fails_with_non_existent_channel_id(
        self, mock_webclient, mock_env_token
    ):
        with pytest.raises(
            SlackChannelNotFoundError,
            match="No channel with name 'not-a-real-channel' found",
        ):
            SlackClient(channel="not-a-real-channel")

    def test_get_channel_id_not_found(self, mock_webclient, mock_env_token):
        client = SlackClient()
        with pytest.raises(
            SlackChannelNotFoundError,
            match="No channel with name 'not-a-real-channel' found",
        ):
            client.get_channel_id_from_name("not-a-real-channel")

    def test_get_channel_id_api_error(self, mock_webclient, mock_env_token):
        stdout = io.StringIO()
        client = SlackClient(stdout=stdout)

        mock_webclient.return_value.conversations_list.side_effect = SlackApiError(
            message="API error", response={"ok": False, "error": "missing_scope"}
        )

        with pytest.raises(SlackApiError, match="missing_scope"):
            client.get_channel_id_from_name("bots")

    def test_send_message_successful(self, mock_webclient, mock_env_token):
        mock_webclient.return_value.chat_postMessage.return_value = Mock(
            data={"ok": True, "ts": "1234567890.123456"}
        )

        client = SlackClient()
        response = client.send_message("test message")

        mock_webclient.return_value.chat_postMessage.assert_called_once_with(
            channel="C123456",
            text="test message",
            thread_ts=None,
            blocks=None,
            icon_emoji=":robot_face:",
            username="WDIV Bot",
        )
        assert response == {"ok": True, "ts": "1234567890.123456"}

    def test_send_message_with_thread(self, mock_webclient, mock_env_token):
        mock_webclient.return_value.chat_postMessage.return_value = Mock(
            data={"ok": True, "ts": "1234567890.123456"}
        )

        client = SlackClient()
        client.send_message("test message", thread_ts="1234567890.123456")

        mock_webclient.return_value.chat_postMessage.assert_called_once_with(
            channel="C123456",
            text="test message",
            thread_ts="1234567890.123456",
            blocks=None,
            icon_emoji=":robot_face:",
            username="WDIV Bot",
        )

    def test_send_message_with_blocks(self, mock_webclient, mock_env_token):
        blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": "test"}}]
        mock_webclient.return_value.chat_postMessage.return_value = Mock(
            data={"ok": True, "ts": "1234567890.123456"}
        )

        client = SlackClient()
        client.send_message("test message", blocks=blocks)

        mock_webclient.return_value.chat_postMessage.assert_called_once_with(
            channel="C123456",
            text="test message",
            thread_ts=None,
            blocks=blocks,
            icon_emoji=":robot_face:",
            username="WDIV Bot",
        )

    def test_send_message_api_error(self, mock_webclient, mock_env_token):
        mock_webclient.return_value.chat_postMessage.side_effect = SlackApiError(
            message="API error", response={"ok": False, "error": "rate_limited"}
        )

        client = SlackClient()
        with pytest.raises(SlackApiError):
            client.send_message("test message")

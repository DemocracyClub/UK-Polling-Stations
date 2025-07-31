import sys

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import os
from typing import Optional, Dict, Any


class SlackChannelNotFoundError(Exception):
    pass


class SlackClient:
    def __init__(
        self,
        token: Optional[str] = None,
        channel: str = "bots",
        stdout=None,
        username: str = "WDIV Bot",
    ):
        self.stdout = stdout or sys.stdout
        self.token = token or os.getenv("SLACK_TOKEN")
        if not self.token:
            raise ValueError(
                "Slack token not provided and SLACK_TOKEN not found in environment"
            )

        self.client = WebClient(token=self.token)
        self.channel = channel
        self.channel_id = self.get_channel_id_from_name(self.channel)
        self.username = username

    def get_channel_id_from_name(self, channel_name: str) -> Optional[str]:
        conversation_id = None
        try:
            conversations_response = self.client.conversations_list()
            for channel in conversations_response.data["channels"]:
                if channel["name"] == channel_name:
                    conversation_id = channel["id"]
                    return conversation_id
        except SlackApiError as e:
            self.stdout.write("Error with Slack API")
            raise e

        if not conversation_id:
            raise SlackChannelNotFoundError(
                f"No channel with name '{channel_name}' found"
            )

    def send_message(
        self,
        message: str,
        thread_ts: Optional[str] = None,
        blocks: Optional[list] = None,
    ) -> Dict[str, Any]:
        try:
            response = self.client.chat_postMessage(
                channel=self.channel_id,
                text=message,
                thread_ts=thread_ts,
                blocks=blocks,
                icon_emoji=":robot_face:",
                username=self.username,
            )

            return response.data

        except SlackApiError as e:
            self.stdout.write(f"Error sending message: {e.response['error']}")
            raise

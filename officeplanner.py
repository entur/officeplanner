import os
import sys
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

with open('channels.txt', 'r') as file:
    channels = [line.rstrip() for line in file]

for line in channels:
    try:
        response = client.chat_postMessage(
            channel=line, text="When are you planning to be in-office next week?")
        assert response["message"]["text"] == "When are you planning to be in-office next week?"
        print(f"Message sent to {line}")

        rs_timestamp = response["ts"]
        rs_channel = response["channel"]

        def reactionAdd(emojis):
            for emoji in emojis:
                time.sleep(1)  # avoiding slack api rate-limiting
                try:
                    client.reactions_add(channel=rs_channel,
                                         timestamp=rs_timestamp, name=f'{emoji}')
                except SlackApiError as e:
                    assert e.response["ok"] is False
                    assert e.response["error"]
                    print(
                        f"Error adding reactions to channel {line}: {e.response['error']}", file=sys.stderr)
                    sys.exit(1)

        emojis = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday"
        ]

        reactionAdd(emojis)
        print(f"Responses added to message in {line}")

    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(
            f"Error posting message in channel {line}: {e.response['error']}", file=sys.stderr)
        sys.exit(1)

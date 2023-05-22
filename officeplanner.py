"""A small scheduled script for posting an in-office indicator to slack"""
import os
import sys
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

GREETING = "When are you planning to be in-office next week?"
OK = "ok"
ERROR = "error"
MSG = "message"
TXT = "text"
TIMESTAMP = "ts"
CHANNEL = "channel"
ASSERT_GREETING = "Expected greeting to verbatim match"
ASSERT_NOT_OK = "Expected response to not be OK"
ASSERT_ERROR = "Expected error state to be true"

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

with open('channels.txt', 'r', encoding='UTF-8') as file:
    channels = [line.rstrip() for line in file]

for channel in channels:
    try:
        api_response = client.chat_postMessage(channel=channel, text=GREETING)
        assert api_response[MSG][TXT] == GREETING, ASSERT_GREETING
        print(f"Message sent to {channel}")

        def add_default_reactions(response, emojis):
            """Add standard reactions, one for each day of the week"""
            for emoji in emojis:
                time.sleep(1)  # avoid slack api rate-limiting
                try:
                    client.reactions_add(
                        channel=response[CHANNEL],
                        timestamp=response[TIMESTAMP],
                        name=f'{emoji}')
                except SlackApiError as sae_emojis:
                    assert sae_emojis.response[OK] is False, ASSERT_NOT_OK
                    assert sae_emojis.response[ERROR], ASSERT_ERROR
                    print(
                        "Error adding reactions to channel",
                        f"{response[CHANNEL]}: {sae_emojis.response[ERROR]}",
                        file=sys.stderr)

        day_of_the_week_emojis = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday"
        ]

        add_default_reactions(api_response, day_of_the_week_emojis)
        print(f"Responses added to message in {channel}")

    except SlackApiError as sae:
        assert sae.response[OK] is False, ASSERT_NOT_OK
        assert sae.response[ERROR], ASSERT_ERROR
        print(
            "Error posting message in channel",
            f"{channel}: {sae.response['error']}",
            file=sys.stderr)
    except AssertionError as ae:
        print(f"Assertion error: {ae}", file=sys.stderr)

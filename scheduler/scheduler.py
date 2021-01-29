import logging
import sys

from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


def my_job():
    client = WebClient(token=settings.SLACK_TOKEN)
    try:
        response = client.chat_postMessage(
            channel='#bot', text="Hello world!")
        assert response["message"]["text"] == "Hello world!"
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        # str like 'invalid_auth', 'channel_not_found'
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")


def start():
    if settings.DEBUG:
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    scheduler.add_job(
        my_job,
        trigger='interval',
        minutes=1,
        id="my_job",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )

    scheduler.start()
    print("Scheduler started...", file=sys.stdout)

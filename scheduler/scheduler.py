import datetime
import logging
import sys
import asyncio

from django.conf import settings
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError

from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


async def post_message(message):
    client = AsyncWebClient(token=settings.SLACK_TOKEN)
    try:
        response = await client.chat_postMessage(
            channel='#bot', text=message)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")


def slack_reminder(start=settings.OPEN_HOUR, end=settings.CLOSE_HOUR, url="beep boop", job_id="slack_reminder"):
    message = "Recuerda elegir tu menu del dia! Link de acceso: " + url

    now = datetime.datetime.now()
    if start < now.hour < end:
        asyncio.run(post_message(message))
    else:
        scheduler.remove_job(job_id)


def start():
    if settings.DEBUG:
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    scheduler.start()
    print("Scheduler started...", file=sys.stdout)

# encoding=utf8
#!/usr/bin/python3

import logging
import random
import requests

from datetime import datetime

from local_config import (
    evening_message,
    lunctime_message,
    early_morning_message,
    late_morning_message,
    other,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    videos
)

logging.basicConfig(filename='telegrambot.log', level=logging.INFO)

telegram_url = 'https://api.telegram.org/bot{}/'.format(TELEGRAM_BOT_TOKEN)

# set up bot and get bot token
# use this url https://api.telegram.org/bot<YourBOTToken>/getUpdates
# get the 'id' of the chat object that is returned - this is the group chat id

options = {
    7: early_morning_message,
    8: late_morning_message,
    11: other,
    13: lunctime_message,
    15: other,
    18: videos,
    23: evening_message
}

def main():

    try:
        hour = datetime.now().hour
        option = options.get(hour)

        if option:
            if hour > 8:
                send_text(random.choice(option))
            else:
                send_text(option)

    except Exception as e:
        dt = datetime.now().strftime("%x %X")
        logging.error(
            "The following error was encountered at {}:"
            "\n{}".format(dt, e)
        )
        send_text(
            "An exception was encountered during the running of the "
            "daily_messenger app. Check the logs :)"
        )


def send_text(text):
    """Sends some text via a bot to the chosen group. Returns
    the request status_code for validating"""
    url = telegram_url + 'sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID,
            'text': text}
    r = requests.post(url, data=data)

    return r.status_code

main()

# def get_updates():
#     """Returns all available updates sent to the bot. Date
#     returned in json format"""
#     url = telegram_url + 'getUpdates'
#
#     return requests.get(url).json()


# def delete_updates(updates):
#     """Cycles through the json updates data and deletes
#     each message."""
#
#     url = telegram_url + 'deleteMessage'
#     for update in updates['result']:
#
#         data = {'chat_id': TELEGRAM_CHAT_ID,
#                 'message_id': update['update_id']}
#         r = requests.post(url, data=data)
#         if r.status_code != 200:
#             raise Exception

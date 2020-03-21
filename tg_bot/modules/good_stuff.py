from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, run_async

import urllib.request, json, random

from tg_bot import dispatcher


@run_async
def dad_joke(bot: Bot, update: Update):
    message = update.effective_message
    dj_request = urllib.request.Request(
        'https://www.reddit.com/r/dadjokes.json',
        data = None, 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    with urllib.request.urlopen(dj_request) as url:
        dj_json = json.loads(url.read().decode())

    pick = random.randint(0, 25)
    head = dj_json['data']['children'][pick]['data']['title']
    body = dj_json['data']['children'][pick]['data']['selftext']

    bot.send_message(
        message.chat.id,
        '*%s*\n%s' % (head, body),
        parse_mode = ParseMode.MARKDOWN
    )

DAD_JOKE_HANDLER = CommandHandler('dadjoke', dad_joke)

dispatcher.add_handler(DAD_JOKE_HANDLER)
from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async

import urllib.request, json, random

from tg_bot import dispatcher
from tg_bot.modules.sql import bruh_sql as sql


class BruhFilter(BaseFilter):
    def filter(self, message):
        if message.text:
            return message.text.lower() == 'bruh' or message.text.lower() == 'bruh moment'
        elif message.sticker:
            return message.sticker.file_id[-26:] == 'AAL9AAPUg2ggEepgeyH76-YYBA'

bruh_filter = BruhFilter()


class WhomstFilter(BaseFilter):
    def filter(self, message):
        return 'kaizoe' in message.text.lower() and ('who' in message.text.lower() or 'what' in message.text.lower())

whomst_filter = WhomstFilter()


class GreetingFilter(BaseFilter):
    def filter(self, message):
        return (
            'kaizoe' in message.text.lower() and 
            (
                'hi' in message.text.lower() or 
                'hey' in message.text.lower() or
                'hello' in message.text.lower()
            )
        )

greeting_filter = GreetingFilter()


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


@run_async
def bruh(bot: Bot, update: Update):
    message = update.effective_message
    bruh_count = sql.new_bruh_moment(message.chat.id)

    bot.send_message(
        message.chat.id,
        'A bruh moment has been reported.\n\n`Total bruh moments in this chat so far: %d`' % (int(bruh_count)),
        parse_mode = ParseMode.MARKDOWN
    )


@run_async
def whomst(bot: Bot, update: Update):
    message = update.effective_message

    message.reply_text(
        'ur mom lmao'
    )


@run_async
def greeting(bot: Bot, update: Update):
    message = update.effective_message

    message.reply_text(
        'Hey %s! Sup?' % (message.from_user.first_name)
    )


DAD_JOKE_HANDLER = CommandHandler('dadjoke', dad_joke)
BRUH_COUNT_HANDLER = MessageHandler(bruh_filter, bruh)
WHOMST_HANDLER = MessageHandler(whomst_filter, whomst)
GREETING_HANDLER = MessageHandler(greeting_filter, greeting)

dispatcher.add_handler(DAD_JOKE_HANDLER)
dispatcher.add_handler(BRUH_COUNT_HANDLER)
dispatcher.add_handler(WHOMST_HANDLER)
dispatcher.add_handler(GREETING_HANDLER)
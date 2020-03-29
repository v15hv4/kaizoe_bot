from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async

import urllib.request, json, random

from tg_bot import dispatcher
from tg_bot.modules.sql import bruh_sql as sql

import random


class BruhFilter(BaseFilter):
    def filter(self, message):
        if message.text:
            return message.text.lower() == 'bruh' or message.text.lower() == 'bruh moment'
        elif message.sticker:
            return message.sticker.file_id[-26:] == 'AAL9AAPUg2ggEepgeyH76-YYBA'

bruh_filter = BruhFilter()


class WhomstFilter(BaseFilter):
    def filter(self, message):
        if message.text:
            if 'kaizoe' in message.text.lower():
                if ('who' in message.text.lower() or 'what' in message.text.lower()):
                    return True

whomst_filter = WhomstFilter()


class GreetingFilter(BaseFilter):
    def filter(self, message):
        if message.text:
            return (
                'kaizoe' in message.text.lower() and 
                (
                    'hi' in message.text.lower() or 
                    'hey' in message.text.lower() or
                    'hello' in message.text.lower()
                )
            )

greeting_filter = GreetingFilter()

class DieFilter(BaseFilter):
    def filter(self,message):
        if message.text:
            if 'kaizoe' in message.text.lower() and 'die' in message.text.lower():
                return True

die_filter = DieFilter()

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
def die(bot: Bot, update: Update):
    message = update.effective_message
    message.reply_text(
        'Go fuck yourself nigga!'
       )

@run_async
def fcoin(bot: Bot, update: Update):
    message = update.effective_message
    res = random.randint(0,1)
    m = 'shit'
    if(res==1):
        m = 'tails.'
    else:
        m = 'heads.'
    message.reply_text(
        'Its %s' % (m)
    )

@run_async
def greeting(bot: Bot, update: Update):
    message = update.effective_message

    message.reply_text(
        'Hey %s! Sup?' % (message.from_user.first_name)
    )

@run_async
def mock(bot: Bot, update: Update):
    message = update.effective_message
    reply = ''.join(word + ' ' for word in message.text.split(' ')[1:])
    if reply:
        reply_id = False
    else:
        reply = message.reply_to_message.text
        reply_id = message.reply_to_message.message_id
    mocked_list = []
    alt_count = 0
    for char in reply:
        if char == ' ':
            mocked_list.append(' ')
        else:
            if alt_count % 2:
                mocked_list.append(char.lower())
            else:
                mocked_list.append(char.upper())
            alt_count += 1
    mocked_message = ''.join(mocked_list)
    bot.send_message(
        message.chat.id,
        mocked_message,
        reply_to_message_id = reply_id
    )


MOCK_HANDLER = CommandHandler('mock', mock)
FLIPCOIN_HANDLER = CommandHandler('fcoin',fcoin)
DAD_JOKE_HANDLER = CommandHandler('dadjoke', dad_joke)
BRUH_COUNT_HANDLER = MessageHandler(bruh_filter, bruh)
WHOMST_HANDLER = MessageHandler(whomst_filter, whomst)
GREETING_HANDLER = MessageHandler(greeting_filter, greeting)
DIE_HANDLER = MessageHandler(die_filter, die)

dispatcher.add_handler(MOCK_HANDLER)
dispatcher.add_handler(DIE_HANDLER)
dispatcher.add_handler(FLIPCOIN_HANDLER)
dispatcher.add_handler(DAD_JOKE_HANDLER)
dispatcher.add_handler(BRUH_COUNT_HANDLER)
dispatcher.add_handler(WHOMST_HANDLER)
dispatcher.add_handler(GREETING_HANDLER)
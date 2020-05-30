from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async

from zalgo_text import zalgo
import urllib.request, json, random, requests, re

from tg_bot import dispatcher
from tg_bot.modules.sql import bruh_sql as sql


class BruhFilter(BaseFilter):
    def filter(self, message):
        if message.text:
            return message.text.lower() == 'bruh' or message.text.lower() == 'bruh moment'

bruh_filter = BruhFilter()


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


@run_async
def define(bot: Bot, update: Update):
    message = update.effective_message
    query = {'term' : ''.join([word + ' ' for word in message.text.split(' ')[1:]]).strip()}
    ud_url = 'https://mashape-community-urban-dictionary.p.rapidapi.com/define'
    headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': "f0e32f8badmsh0b2fa1d896283f6p1a3cc4jsnd24d74fcd0b2"
    }
    try:
        response = requests.request('GET', ud_url, headers = headers, params = query)
        response_dict = json.loads(response.text)
        topdef = response_dict['list'][0]
        message.reply_text(
            '[%s:](%s)\n\n%s\n\n_%s_' % (
                topdef['word'],
                topdef['permalink'],
                re.sub('[\[\]]', '', topdef['definition']),
                re.sub('[\[\]]', '', topdef['example'])
            ),
            parse_mode = ParseMode.MARKDOWN,
            disable_web_page_preview = True
        )
    except:
        message.reply_text(
            '¯\_(ツ)_/¯'
        )


@run_async
def zalgofy(bot: Bot, update: Update):
    message = update.effective_message
    reply = ''.join(word + ' ' for word in message.text.split(' ')[1:])
    if reply:
        reply_id = False
    else:
        reply = message.reply_to_message.text
        reply_id = message.reply_to_message.message_id
    cursed_message = zalgo.zalgo().zalgofy(reply)
    bot.send_message(
        message.chat.id,
        cursed_message,
        reply_to_message_id = reply_id
    )


@run_async
def shrug(bot: Bot, update: Update):
    message = update.effective_message
    message.reply_text('¯\_(ツ)_/¯')


SHRUG_HANDLER = CommandHandler('shrug', shrug)
DEFINE_HANDLER = CommandHandler('define', define)
MOCK_HANDLER = CommandHandler('mock', mock)
FLIPCOIN_HANDLER = CommandHandler('fcoin',fcoin)
ZALGOFY_HANDLER = CommandHandler('zalgofy', zalgofy)
DAD_JOKE_HANDLER = CommandHandler('dadjoke', dad_joke)
BRUH_COUNT_HANDLER = MessageHandler(bruh_filter, bruh)
GREETING_HANDLER = MessageHandler(greeting_filter, greeting)

dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(DEFINE_HANDLER)
dispatcher.add_handler(MOCK_HANDLER)
dispatcher.add_handler(FLIPCOIN_HANDLER)
dispatcher.add_handler(ZALGOFY_HANDLER)
dispatcher.add_handler(DAD_JOKE_HANDLER)
dispatcher.add_handler(BRUH_COUNT_HANDLER)
dispatcher.add_handler(GREETING_HANDLER)
from telegram import ParseMode, Update, Bot, Chat, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async, CallbackQueryHandler

from tg_bot import dispatcher

import requests
from parsel import Selector

import json
from urllib.request import urlopen


def imdb_searchdata(bot: Bot, update: Update):
    query = update.callback_query
    title = ''
    rating = ''
    date = ''
    synopsis = ''
    url_sel = 'https://www.imdb.com/title/%s/' % (query.data)
    text_sel = requests.get(url_sel).text
    selector_global = Selector(text = text_sel)
    title = selector_global.xpath('//div[@class="title_wrapper"]/h1/text()').get().strip()
    try:
        rating = selector_global.xpath('//div[@class="ratingValue"]/strong/span/text()').get().strip()
    except:
        rating = '-'
    try:
        date = '(' + selector_global.xpath('//div[@class="title_wrapper"]/h1/span/a/text()').getall()[-1].strip() + ')'
    except:
        date = selector_global.xpath('//div[@class="subtext"]/a/text()').getall()[-1].strip()
    try:
        synopsis = selector_global.xpath('//div[@class="summary_text"]/text()').get().strip()
    except:
        synopsis = '_No synopsis available._'
    movie_data = '*%s*, _%s_\n★ *%s*\n\n%s' % (title, date, rating, synopsis)
    query.edit_message_text(
        movie_data, 
        parse_mode=ParseMode.MARKDOWN
    )

@run_async
def imdb(bot: Bot, update: Update, args):
    message = update.effective_message
    query = ''.join([arg + '_' for arg in args]).lower()
    if not query:
        bot.send_message(
            message.chat.id,
            'You need to specify a movie/show name!'
        )
        return
    url_suggs = 'https://v2.sg.media-imdb.com/suggests/%s/%s.json' % (query[0], query)
    json_url = urlopen(url_suggs)
    suggs_raw = ''
    for line in json_url:
        suggs_raw = line
    skip_chars = 6 + len(query)
    suggs_dict = json.loads(suggs_raw[skip_chars:][:-1])
    if suggs_dict:
        button_list = [[
                InlineKeyboardButton(
                    text = str(sugg['l'] + ' (' + str(sugg['y']) + ')'), 
                    callback_data = str(sugg['id'])
                )] for sugg in suggs_dict['d'] if 'y' in sugg
        ]
        reply_markup = InlineKeyboardMarkup(button_list)
        bot.send_message(
            message.chat.id,
            'Which one? ',
            reply_markup = reply_markup
        )
    else:
        pass


__mod_name__ = 'IMDb'

IMDB_HANDLER = CommandHandler('imdb', imdb, pass_args=True)
IMDB_SEARCHDATA_HANDLER = CallbackQueryHandler(imdb_searchdata)

dispatcher.add_handler(IMDB_HANDLER)
dispatcher.add_handler(IMDB_SEARCHDATA_HANDLER)
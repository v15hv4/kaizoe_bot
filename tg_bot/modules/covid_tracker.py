from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async

from tg_bot import dispatcher

import requests
from parsel import Selector


def cov(bot: Bot, update: Update):
    country = ''
    confirmed = 0
    deceased = 0
    recovered = 0
    message = update.effective_message
    selected = (''.join([message.text.split(' ')[i] + ' ' for i in range(1, len(message.text.split(' ')))])).strip()
    url = 'https://ncov2019.live/'
    text = requests.get(url).text
    selector = Selector(text = text)
    table = selector.css('#sortable_table_Global')
    rows = table.css('tr')
    if not selected:
        country = country = rows[1].css('.text--gray::text').getall()[0].strip()
        confirmed = rows[1].css('.text--green::text').getall()[0].strip()
        deceased = rows[1].css('.text--red::text').getall()[0].strip()
        recovered = rows[1].css('.text--blue::text').getall()[0].strip()
    else:
        for row in rows[2:]:
            country = row.css('.text--gray::text').getall()[1].strip()
            if country.lower() == selected.lower():
                confirmed = row.css('.text--green::text').getall()[0].strip()
                deceased = row.css('.text--red::text').getall()[0].strip()
                recovered = row.css('.text--blue::text').getall()[0].strip()
                break
            country = selected

    bot.send_message(
        message.chat.id,
        '`COVID-19 Tracker`\n*Number of confirmed cases in %s:* %s\n*Deceased:* %s\n*Recovered:* %s\n\n_Source:_ ncov2019.live' % (country, confirmed, deceased, recovered),
        parse_mode = ParseMode.MARKDOWN,
        disable_web_page_preview = True
    )

__help__ = """
*Admin only:*
 - /cov <country>: Get real time COVID-19 stats for the input country
"""

__mod_name__ = 'COVID-19 Tracker'

COV_HANDLER = CommandHandler('cov', cov)

dispatcher.add_handler(COV_HANDLER)
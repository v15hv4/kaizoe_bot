from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async

from tg_bot import dispatcher

import requests
from parsel import Selector

import json
from urllib.request import urlopen

def cov(bot: Bot, update: Update):
    country = ''
    confirmed = 0
    deceased = 0
    recovered = 0
    message = update.effective_message
    selected = (''.join([message.text.split(' ')[i] + ' ' for i in range(1, len(message.text.split(' ')))])).strip()
    url_global = 'https://ncov2019.live/'
    text_global = requests.get(url_global).text
    selector_global = Selector(text = text_global)
    table = selector_global.css('#sortable_table_Global')
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
            country = ''

    bot.send_message(
        message.chat.id,
        '`COVID-19 Tracker`\n*Number of confirmed cases in %s:* %s\n*Deceased:* %s\n*Recovered:* %s\n\n_Source:_ ncov2019.live' % (country, confirmed, deceased, recovered),
        parse_mode = ParseMode.MARKDOWN,
        disable_web_page_preview = True
    )

def covindia(bot: Bot, update: Update):
    message = update.effective_message
    state_list = [
        'Andaman and Nicobar Islands',
        'Andhra Pradesh',
        'Assam',
        'Bihar',
        'Chandigarh',
        'Chattisgarh',
        'Dadar and Nagar Haveli',
        'Daman and Diu',
        'Delhi',
        'Goa',
        'Gujarat',
        'Haryana',
        'Himachal Pradesh',
        'Jammu and Kashmir',
        'Jharkand',
        'Karnataka',
        'Kerala',
        'Ladakh',
        'Lakshadweep',
        'Madhya Pradesh',
        'Maharashtra',
        'Manipur',
        'Meghalaya',
        'Mizoram',
        'Nagaland',
        'Odisha',
        'Puducherry',
        'Punjab',
        'Rajasthan',
        'Sikkim',
        'Tamil Nadu',
        'Telangana',
        'Tripura',
        'Uttar Pradesh',
        'Uttarakhand',
        'West Bengal'
    ]
    state = ''
    confirmed = 0
    deceased = 0
    recovered = 0
    state_input = ''.join([message.text.split(' ')[i] + ' ' for i in range(1, len(message.text.split(' ')))]).strip()
    if state_input:
        for state_check in state_list:
            if state_check.lower() == state_input.lower():
                state = state_check
        selected = (state.split(' ')[0] + ''.join(['+' + state.split(' ')[i] for i in range(1, len(state.split(' ')))]))
        url_india = 'http://portal.covid19india.org/export?diagnosed_date=&detected_state=%s&detected_city=&gender=&current_status=&submit=Apply+Filters&_export=json' % (selected)
        json_url = urlopen(url_india)
        state_dict = json.loads(json_url.read())
        for entry in state_dict:
            confirmed += 1
            if entry['Current status'] == 'Deceased':
                deceased += 1
            elif entry['Current status'] == 'Recovered':
                recovered += 1
        state = state_dict[0]['Detected state']

        bot.send_message(
            message.chat.id,
            '`COVID-19 Tracker`\n*Number of confirmed cases in %s:* %s\n*Deceased:* %s\n*Recovered:* %s\n\n_Source:_ covid19india.org' % (state, confirmed, deceased, recovered),
            parse_mode = ParseMode.MARKDOWN,
            disable_web_page_preview = True
        )
    else:
        bot.send_message(
            message.chat.id,
            'You need to specify a valid Indian state!',
            parse_mode = ParseMode.MARKDOWN,
            disable_web_page_preview = True
        )

__help__ = """
*Admin only:*
 - /cov <country>: Get real time COVID-19 stats for the input country
 - /covindia <state>: Get real time COVID-19 stats for the input Indian state
"""

__mod_name__ = 'COVID-19 Tracker'

COV_HANDLER = CommandHandler('cov', cov)
COV_INDIA_HANDLER = CommandHandler('covindia', covindia)

dispatcher.add_handler(COV_HANDLER)
dispatcher.add_handler(COV_INDIA_HANDLER)
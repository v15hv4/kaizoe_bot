from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async

from tg_bot import dispatcher
from tg_bot import COVID_193_API_KEY

import requests
from parsel import Selector

import os
import json
from urllib.request import urlopen


def cov(bot: Bot, update: Update):
    message = update.effective_message
    country = ''
    new = 0
    confirmed = 0
    deceased = 0
    recovered = 0
    country_input = ''.join([message.text.split(' ')[i] + ' ' for i in range(1, len(message.text.split(' ')))]).strip()

    if not country_input:
        country_input = 'all'
    
    url_global = "https://covid-193.p.rapidapi.com/statistics"
    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': COVID_193_API_KEY
    }
    json_response = requests.get(url_global, headers = headers)
    global_dict = json.loads(json_response.text)
    
    if country_input.lower()[:3] == 'top':
        try:
            n = int(country_input.lower()[3:])
            name_list = []
            conf_list = []
            for i in range(0, n):
                name_list.append(global_dict['response'][i]['country'].replace('-', ' '))
                conf_list.append(global_dict['response'][i]['cases']['total'])
            out_list = ''
            for i in range(0, n):
                out_list += '%s\t\t%s\n' % (name_list[i], format(int(conf_list[i]), ',d'))
            bot.send_message(
                message.chat.id,
                '`COVID-19 Tracker:`\n\n' + out_list + '\n\n_Source:_ api-sports.io',
                parse_mode = ParseMode.MARKDOWN,
                disable_web_page_preview = True
            )
            return
        except:
            bot.send_message(
                message.chat.id,
                'Invalid argument!'
            )
            return


    for gdict in global_dict['response']:
        if gdict['country'].lower().replace('-', ' ') == country_input.lower():
            new = gdict['cases']['new'][1:]
            confirmed = gdict['cases']['total']
            deceased = gdict['deaths']['total']
            recovered = gdict['cases']['recovered']
            country = gdict['country'].replace('-', ' ')
            break

    if country.lower() == 'all':
        country = 'global'
    elif not country:
        country = country_input

    bot.send_message(
        message.chat.id,
        '`COVID-19 Tracker:` *%s*\n\n*Confirmed:* %s   _(+%s in the past 24 hrs)_\n*Deceased:* %s\n*Recovered:* %s\n\n_Source:_ api-sports.io' % (
            country.upper(),
            format(int(confirmed), ',d'),
            format(int(new), ',d'),
            format(int(deceased), ',d'),
            format(int(recovered), ',d')
        ),
        parse_mode = ParseMode.MARKDOWN,
        disable_web_page_preview = True
    )


def covindia(bot: Bot, update: Update):
    message = update.effective_message
    state = ''
    new = 0
    confirmed = 0
    deceased = 0
    recovered = 0
    state_input = ''.join([message.text.split(' ')[i] + ' ' for i in range(1, len(message.text.split(' ')))]).strip()
    if state_input:
        url_india = 'https://api.covid19india.org/data.json'
        json_url = urlopen(url_india)
        state_dict = json.loads(json_url.read())
        for sdict in state_dict['statewise']:
            if sdict['state'].lower() == state_input.lower():
                new = sdict['delta']['confirmed']
                confirmed = sdict['confirmed']
                deceased = sdict['deaths']
                recovered = sdict['recovered']
                state = sdict['state']
                break
    
    if state:
        bot.send_message(
            message.chat.id,
            '`COVID-19 Tracker:` *%s*\n\n*Confirmed:* %s   _(+%s in the past 24 hrs)_\n*Deceased:* %s\n*Recovered:* %s\n\n_Source:_ covid19india.org' % (
                state.upper(),
                format(int(confirmed), ',d'),
                format(int(new), ',d'),
                format(int(deceased), ',d'),
                format(int(recovered), ',d')
            ),
            parse_mode = ParseMode.MARKDOWN,
            disable_web_page_preview = True
        )
    else:
        bot.send_message(
            message.chat.id,
            'You need to specify a valid Indian state!'
        )


__help__ = """
 - /cov <country>: Get real time COVID-19 stats for the input country
 - /covindia <state>: Get real time COVID-19 stats for the input Indian state
"""

__mod_name__ = 'COVID-19 Tracker'

COV_HANDLER = CommandHandler('cov', cov)
COV_INDIA_HANDLER = CommandHandler('covindia', covindia)

dispatcher.add_handler(COV_HANDLER)
dispatcher.add_handler(COV_INDIA_HANDLER)
from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async

from tg_bot import dispatcher

import os
import json
import re
import sys
from json import load
from parsel import Selector
from requests import session
from datetime import datetime
from requests.utils import requote_uri
import base64

# initiate session
s = session()

# utils {{{
# course name shortener
def parse_course(raw):
    if len(raw) > 15:
        return re.sub(r"[a-z, ]", "", raw)
    return raw

# login to moodle via CAS {{{
def login():
    host = "https://login.iiit.ac.in/cas/login"
    service = "https://courses.iiit.ac.in/login/index.php?authCAS=CAS"

    usr_enc = b'\x61\x6e\x69\x72\x76\x69\x6e\x79\x61\x2e\x67\x75\x72\x75\x72\x61\x6a\x61\x6e\x40\x72\x65\x73\x65\x61\x72\x63\x68\x2e\x69\x69\x69\x74\x2e\x61\x63\x2e\x69\x6e'
    pass_enc = b'\x56\x69\x67\x6e\x65\x73\x68\x40\x31\x32\x33'
    username = usr_enc.decode('utf-8')
    password = pass_enc.decode('utf-8')

    page = s.get(host).text

    # get execution attribute
    execution_re = r'<input type="hidden" name="execution" value="([^<]*)"/>'
    execution = re.findall(execution_re, page, re.M)[0]

    # log user in and store cookies in session
    login = s.post(
        requote_uri(f"{host}?service={service}"),
        data={
            "username": username,
            "password": password,
            "execution": execution,
            "_eventId": "submit",
            "geolocation": "",
        },
    )

    # open moodle
    moodle = s.get(service)


# }}}

# get upcoming events {{{
def upcoming_function():
    url = "https://courses.iiit.ac.in/calendar/view.php?view=upcoming"

    XPATHS = {
        "events": r"//div[contains(@class, 'eventlist')]/div[contains(@class, 'event')]",
        "date": r".//div[@class='row']/div[@class='col-11']/a/text()",
        "time": r".//div[@class='row']/div[@class='col-11']/text()",
        "title": r".//h3/text()",
        "course": r".//div[@class='row mt-1']/div[@class='col-11']/a/text()",
    }

    res = s.get(url)
    events = list(
        map(
            lambda e: {
                "date": e.xpath(XPATHS["date"]).get(),
                "time": e.xpath(XPATHS["time"]).get(),
                "title": e.xpath(XPATHS["title"]).get(),
                "course": parse_course(e.xpath(XPATHS["course"]).get()),
            },
            Selector(text=res.text).xpath(XPATHS["events"]),
        )
    )

    to_return_string = ""

    for event in events:
        to_return_string += (event["date"] + ' ' + event["time"] + '\n' + event["course"] + '\n' + event["title"] + '\n\n')

    return to_return_string


@run_async
def upcoming(bot: Bot, update: Update):
    message = update.effective_message
    try:
        login()

        message.reply_text(
            upcoming_function()
        )

    except:
        message.reply_text(
            '¯\_(ツ)_/¯'
        )

DEADLINE_HANDLER = CommandHandler('upcoming', upcoming)

dispatcher.add_handler(DEADLINE_HANDLER)

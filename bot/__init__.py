import os
import sys
import logging

from pyrogram import Client

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    try:
        API_ID = int(os.environ.get("API_ID", None))
    except ValueError:
        raise Exception("Invalid API_ID!")

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Invalid OWNER_ID!")

    API_HASH = os.environ.get("API_HASH", None)
    USE_BOT_API = os.environ.get("USE_BOT_API", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    PHONE_NUMBER = os.environ.get("PHONE_NUMBER", None)
    SESSION_NAME = os.environ.get("SESSION_NAME", None)
    COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", None)
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "").split()

else:
    from bot.config import (
        API_ID,
        OWNER_ID,
        API_HASH,
        USE_BOT_API,
        BOT_TOKEN,
        PHONE_NUMBER,
        SESSION_NAME,
        COMMAND_PREFIX,
        LOAD,
        NO_LOAD,
    )

    try:
        API_ID = int(API_ID)
    except ValueError:
        raise Exception("Invalid API_ID!")

    try:
        OWNER_ID = int(OWNER_ID)
    except ValueError:
        raise Exception("Invalid OWNER_ID!")

if USE_BOT_API:
    CLIENT = Client(
        session_name=SESSION_NAME,
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
    )
else:
    CLIENT = Client(
        session_name=SESSION_NAME,
        api_id=API_ID,
        api_hash=API_HASH,
        phone_number=PHONE_NUMBER,
    )

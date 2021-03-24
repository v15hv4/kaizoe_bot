import os
import sys
import logging

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
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    SESSION_NAME = os.environ.get("SESSION_NAME", None)
    COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", None)

else:
    from bot.config import API_ID, OWNER_ID, API_HASH, BOT_TOKEN, SESSION_NAME, COMMAND_PREFIX

    try:
        API_ID = int(API_ID)
    except ValueError:
        raise Exception("Invalid API_ID!")

    try:
        OWNER_ID = int(OWNER_ID)
    except ValueError:
        raise Exception("Invalid OWNER_ID!")

import asyncio
import importlib

from bot import LOGGER, CLIENT
from bot.modules import ALL_MODULES


IMPORTED = {}
HELPABLE = {}

# import modules
for module_name in ALL_MODULES:
    imported_module = importlib.import_module(f"bot.modules.{module_name}")
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name!")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module


# default commands
# @client.on_message()
# async def replytoallmessages(_, message):
#     await message.reply_text("hey")


if __name__ == "__main__":
    LOGGER.info(f"Successfully loaded: {str(ALL_MODULES)}")
    CLIENT.run()

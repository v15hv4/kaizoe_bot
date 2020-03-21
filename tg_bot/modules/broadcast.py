from time import sleep

from telegram import Update, Bot
from tg_bot import dispatcher, LOGGER
import tg_bot.modules.sql.users_sql as sql
from telegram import TelegramError, Chat, Message
from telegram.ext import CommandHandler, run_async


@run_async
def broadcast(bot: Bot, update: Update):
    message_args = update.effective_message.text.split("\"", 1)
    chats = message_args[0][11:].split(",")[:-1]
    to_send = str(message_args[1])[:-1] + "\n\n:: @" + update.effective_user.username
    if len(to_send) >= 2:
        failed = 0
        for chat in chats:
            try:
                bot.sendMessage(int(chat), to_send)
                sleep(0.1)
            except TelegramError:
                failed += 1
                LOGGER.warning("Couldn't send broadcast to %s", str(chat))
        update.effective_message.reply_text("Broadcast complete. {} groups failed to receive the message.".format(failed))


__help__ = ""

__mod_name__ = "Broadcast"

BROADCAST_HANDLER = CommandHandler("broadcast", broadcast)

dispatcher.add_handler(BROADCAST_HANDLER)
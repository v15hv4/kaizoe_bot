from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, run_async

from tg_bot import dispatcher

import os
from gtts import gTTS


@run_async
def say(bot: Bot, update: Update):
    message = update.effective_message
    text = " ".join(message.text.split(" ")[1:])
    tts_id = "tts_%s_%s.mp3" % (str(message.chat.id), str(message.message_id))
    tts = gTTS(text, lang="en-us")
    tts.save(tts_id)
    bot.send_voice(
        message.chat.id, voice=open(tts_id, "rb"), reply_to_message_id=message.message_id
    )
    os.remove(tts_id)


__mod_name__ = "TTS"

SAY_HANDLER = CommandHandler("say", say)

dispatcher.add_handler(SAY_HANDLER)

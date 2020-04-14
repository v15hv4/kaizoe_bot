from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async

from tg_bot import dispatcher

import os
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '128',
        }],
    'logger': MyLogger(),
    'outtmpl': '%(title)s.%(ext)s'
}


@run_async
def ytdl(bot: Bot, update: Update):
    message = update.effective_message
    target_urls = message.text.split(' ')[1]
    progress_message = bot.send_message(
        message.chat.id,
        'Downloading, hold on...',
        reply_to_message_id = message.message_id
    )
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_urls, download = True)
            filename = ydl.prepare_filename(info)[:-4] + 'mp3'
        bot.send_audio(
            message.chat.id,
            audio = open(filename, 'rb'),
            timeout = 60,
            reply_to_message_id = message.message_id
        )
        bot.delete_message(
            progress_message.chat.id,
            progress_message.message_id
        )
        os.remove(filename)
        return
    except:
        bot.edit_message_text(
            'Download failed!',
            progress_message.chat.id,
            progress_message.message_id
        )
        return

__help__ = """
 - /ytdl <link>: Download audio from the YouTube link provided
"""

__mod_name__ = 'YouTube Audio Downloader'

YTDL_HANDLER = CommandHandler('ytdl', ytdl)

dispatcher.add_handler(YTDL_HANDLER)
from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, run_async
from PIL import Image
from math import ceil
import os

from tg_bot import dispatcher


@run_async
def add_sticker(bot: Bot, update: Update):
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    try:
        args = message.text.split(' ')[1]
    except:
        args = 'personal'
    if args.lower() == 'group':
        set_name = 'pack_' + str(chat.id)[1:] + '_by_' + bot.username
    else:
        set_name = 'pack_' + str(user.id)[1:] + '_by_' + bot.username
    if message.reply_to_message.sticker:
        file_id = message.reply_to_message.sticker.file_id
        sticker_file = bot.get_file(file_id)
        sticker_file.download('sticker_input.png')
    elif message.reply_to_message.photo:
        file_id = message.reply_to_message.photo[-1].file_id
        sticker_file = bot.get_file(file_id)
        sticker_file.download('sticker_input.png')
        sticker = Image.open('sticker_input.png')
        if sticker.width < 512 and sticker.height < 512:
            if sticker.width < sticker.height:
                asp_ratio = sticker.width / sticker.height
                sticker = sticker.resize((ceil(asp_ratio * 512), 512))
            else:
                asp_ratio = sticker.height / sticker.width
                sticker = sticker.resize((512, ceil(asp_ratio * 512)))
        else:
            sticker.thumbnail((512, 512))
        sticker.save('sticker_input.png')
        print(sticker.width, sticker.height)
    else:
        message.reply_text('bruh')
        return
    sticker_target = 'sticker_input.png'
    sticker_emoji = '👌'
    
    try:
        set_target = bot.get_sticker_set(set_name)
        sticker_added = bot.add_sticker_to_set(
            user.id,
            set_name,
            png_sticker = open(sticker_target, 'rb'),
            emojis = sticker_emoji
        )
        if sticker_added:
            bot.send_message(
                message.chat.id,
                'Added to [%s](t.me/addstickers/%s).' % (set_target.title, set_name),
                parse_mode = ParseMode.MARKDOWN,
                reply_to_message_id = message.reply_to_message.message_id
            )
    except:
        if args.lower() == 'group':
            set_title = str(chat.title) + ' Stickers'
        else:
            set_title = str(user.username) + '\'s Stickers'
        set_created = bot.create_new_sticker_set(
            user.id,
            set_name,
            set_title,
            png_sticker = open(sticker_target, 'rb'),
            emojis = sticker_emoji
        )
        if set_created:
            bot.send_message(
                message.chat.id,
                'Added to new pack: [%s](t.me/addstickers/%s).' % (set_title, set_name),
                parse_mode = ParseMode.MARKDOWN,
                reply_to_message_id = message.reply_to_message.message_id
            )

    os.remove('sticker_input.png')


__mod_name__ = 'Stickers'

ADD_STICKER_HANDLER = CommandHandler('addsticker', add_sticker)

dispatcher.add_handler(ADD_STICKER_HANDLER)
from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, run_async
from telegram.error import RetryAfter

import os
import urllib.request
from math import ceil
from PIL import Image, ImageDraw, ImageFont, ImageOps

from tg_bot import dispatcher
from tg_bot import UNIV_STICKER_OWNER_ID, ATAF_FONT_URL


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
    elif message.reply_to_message.text:
        target_text = message.reply_to_message.text
        target_from = message.reply_to_message.from_user
        target_name = target_from.first_name
        target_file = str(message.reply_to_message.message_id) + '.png'
        target_ppic = target_from.get_profile_photos().photos[0][0].get_file()
        target_ppic.download(target_file)
        parts = []
        padding = 100
        linelen = 0
        offset = 20
        nrows = 1
        ncols = 1
        line = ''
        for word in target_text.split(' '):
            linelen += len(word)
            if linelen < 35:
                line = line + word + ' '
                if linelen > ncols:
                    ncols = linelen
            else:
                parts.append(line.strip())
                linelen = 0
                line = word + ' '
        parts.append(line)
        nrows = len(parts)
        if len(target_name) > ncols:
            ncols = len(target_name)

        IMG_WIDTH = ncols * 11 + padding + 30
        IMG_HEIGHT = (nrows + 1) * 20 + padding - 40
        BUBBLE_WIDTH = ncols * 11 + padding + 20
        BUBBLE_HEIGHT = (nrows + 1) * 20 + padding - 50
        corner = Image.new('RGB', (10, 10), (0, 0, 0))
        drawcorner = ImageDraw.Draw(corner)
        drawcorner.pieslice((0, 0, 20, 20), 180, 270, fill='#212121')
        bubble = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), (0, 0, 0))
        fnt_name = ImageFont.truetype('Roboto-Medium.ttf', 18)
        fnt_msg = ImageFont.truetype('Roboto-Regular.ttf', 18)
        draw = ImageDraw.Draw(bubble)
        draw.rectangle(((60, 10), (BUBBLE_WIDTH, BUBBLE_HEIGHT)), fill='#212121')
        bubble.paste(corner, (60, 10))
        bubble.paste(corner.rotate(90), (60, BUBBLE_HEIGHT - 9))
        bubble.paste(corner.rotate(180), (BUBBLE_WIDTH - 9, BUBBLE_HEIGHT - 9))
        bubble.paste(corner.rotate(270), (BUBBLE_WIDTH - 9, 10))
        draw.text((75, 22), target_name, font = fnt_name)
        for idx, inp in enumerate(parts):
            draw.text((75, 48 + (offset * idx)), inp, font = fnt_msg)
        ppic = Image.open(target_file)
        ppic.resize((40, 40))
        bigsize = (ppic.size[0] * 3, ppic.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        drawmask = ImageDraw.Draw(mask)
        drawmask.ellipse((0, 0) + bigsize, fill = 255)
        mask = mask.resize(ppic.size, Image.ANTIALIAS)
        ppic.putalpha(mask)
        ppic_circ = ImageOps.fit(ppic, mask.size, centering = (0.5, 0.5))
        ppic_circ.putalpha(mask)
        ppic_circ.thumbnail((36, 36))
        bubble.paste(ppic_circ, (10, IMG_HEIGHT - 50))
        if bubble.width < 512 and bubble.height < 512:
            if bubble.width < bubble.height:
                asp_ratio = bubble.width / bubble.height
                bubble = bubble.resize((ceil(asp_ratio * 512), 512))
            else:
                asp_ratio = bubble.height / bubble.width
                bubble = bubble.resize((512, ceil(asp_ratio * 512)))
        else:
            bubble.thumbnail((512, 512))
        bubble.save(str(message.message_id) + '.webp')
        bot.send_document(
            message.chat.id,
            document = open(str(message.message_id) + '.webp', 'rb'),
            reply_to_message_id = message.message_id
        )
        os.remove(target_file)
        os.remove(str(message.message_id) + '.webp')
        return
    else:
        message.reply_text('bruh')
        return
    sticker_target = 'sticker_input.png'
    sticker_emoji = '👌'
    
    try:
        set_target = bot.get_sticker_set(set_name)
        sticker_added = bot.add_sticker_to_set(
            user_id = user.id,
            name = set_name,
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
    except RetryAfter:
        bot.send_message(
            message.chat.id,
            'Slow down! Try again in 10 seconds.'
        )
    except:
        if args.lower() == 'group':
            set_title = str(chat.title) + ' Stickers'
        else:
            set_title = str(user.username) + '\'s Stickers'
        try:
            set_created = bot.create_new_sticker_set(
                user_id = user.id,
                name = set_name,
                title = set_title,
                png_sticker = open(sticker_target, 'rb'),
                emojis = sticker_emoji
            )
        except:
            set_created = bot.create_new_sticker_set(
                user_id = UNIV_STICKER_OWNER_ID,
                name = set_name,
                title = set_title,
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

@run_async
def ataf(bot: Bot, update: Update):
    message = update.effective_message
    limit = 170
    inp_str = (''.join(sen + ' ' for sen in message.text.split(' ')[1:])).strip()
    if(len(inp_str) > limit):
        message.reply_text('Character limit exceeded!')
        return
    ataf_id = 'ataf_%s_%s.webp' % (str(message.chat.id), str(message.message_id))
    if not os.path.isfile('ataf.jpg'):
        urllib.request.urlretrieve('https://i.imgur.com/zq0nINE.jpg', 'ataf.jpg')
    if not os.path.isfile('B612Mono-Regular.ttf'):
        urllib.request.urlretrieve(ATAF_FONT_URL, 'B612Mono-Regular.ttf')
    img = Image.open('ataf.jpg')
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('B612Mono-Regular.ttf', 18)
    n = 22
    parts = [
        inp_str[i:i + n] + '-' 
        if inp_str[i:i + n + 1][-1] != ' '
        else inp_str[i:i + n] 
        for i in range(0, len(inp_str), n)
    ]
    parts[-1] = parts[-1][:-1]
    offset = 20
    for idx, inp in enumerate(parts):
        d.text((265, 50 + (offset * idx)), inp, font = fnt, fill = (0, 0, 0))
    if img.width < 512 and img.height < 512:
        if img.width < img.height:
            asp_ratio = img.width / img.height
            img = img.resize((ceil(asp_ratio * 512), 512))
        else:
            asp_ratio = img.height / img.width
            img = img.resize((512, ceil(asp_ratio * 512)))
    else:
        img.thumbnail((512, 512))
    img.save(ataf_id)
    bot.send_document(
        message.chat.id,
        document = open(ataf_id, 'rb'),
        reply_to_message_id = message.message_id
    )
    os.remove(ataf_id)

__help__ = """
 - <reply> /addsticker personal: Add replied-to sticker to your personal pack (Default)
 - <reply> /addsticker group: Add replied-to sticker to current group's pack
"""

__mod_name__ = 'Stickers'

ADD_STICKER_HANDLER = CommandHandler('addsticker', add_sticker)
ATAF_HANDLER = CommandHandler('ataf', ataf)

dispatcher.add_handler(ADD_STICKER_HANDLER)
dispatcher.add_handler(ATAF_HANDLER)
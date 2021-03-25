from pyrogram import filters
from bot import CLIENT as client, COMMAND_PREFIX as prefix


@client.on_message(filters.regex(f"^(?i)((hey|hi|hello|sup) kaizoe)"))
async def greeting(_, message):
    await message.reply_text(f"Hey {message.from_user.first_name}! Sup?")


@client.on_message(filters.regex(f"^{prefix}.*"))
async def handle_command(_, message):
    command, *args = message.text.split(" ")
    await message.reply_text(f"The {command} command with arguments {str(args)} is undefined.")

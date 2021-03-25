from bot import CLIENT as client


@client.on_message()
async def dothis(_, message):
    await message.reply_text("sup")

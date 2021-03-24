import asyncio
from pyrogram import Client

from bot import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME

client = Client(session_name=SESSION_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@client.on_message()
async def hey(_, message):
    await client.send_message(-588968921, "hey")


client.run()

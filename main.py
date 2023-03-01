from aiogram import Bot, executor
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import logging
import os
from checker import mfa_parse

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = Bot(token=BOT_TOKEN)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot, storage=MemoryStorage())

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()

CHANNEL_USERNAME = os.environ['CHANNEL_USERNAME']


async def checker(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        file = open("last.txt", "r")
        last = file.read()
        curr = mfa_parse()
        if curr['text'] != last:
            file.close()
            file = open("last.txt", "w")
            file.write(curr['text'])
            await bot.send_message(CHANNEL_USERNAME, f"{curr['text']}\n{curr['link']}")
        file.close()


if __name__ == '__main__':
    asyncio.ensure_future(checker(30))
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

from aiogram import Bot, executor
from aiogram.types import Message
from aiogram.contrib.middlewares.logging import LoggingMiddleware
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
  asyncio.ensure_future(checker(60))
  executor.start_polling(dp, skip_updates=True)

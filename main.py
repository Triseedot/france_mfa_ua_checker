from aiogram import Bot, executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
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

counter = 0


@dp.message_handler(content_types=['text'])
async def answer_command(message: Message):
    await message.answer('Online')


async def checker(wait_for):
    global counter
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
        if counter == 0:
            print('Online')
            print('Debug text:', curr['text'])
            counter = 21
        counter -= 1
        file.close()


if __name__ == '__main__':
    asyncio.ensure_future(checker(30))
    executor.start_polling(dp, skip_updates=True)

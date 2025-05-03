import logging
import asyncio
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
@dp.message(Command('help'))
async def send_welcome(message: types.Message):
    await message.reply("This is an automized tech support bot for Re2ake! Ask me any questions and I'll try my best to help you by pointing to an FAQ or forwarding your question to the operator.")

@dp.message()
async def on_message(message: types.Message):
    # await message.answer(message.text)
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/ask', params={'q': message.text}) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('answer'):
                    await message.answer(data['answer'])
                else:
                    await message.answer("I couldn't find an answer to your question. I'll forward it to the operator.")
            else:
                await message.answer("There was an error processing your request. Please try again later.")

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
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
    # forward our question to the backend API for an answer
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/ask', params={'q': message.text, 'user_id': message.chat.id, 'message_id': message.message_id}) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('isSuccess'):
                    await message.answer(data['answer'], reply_to_message_id=message.message_id)
                else:
                    await message.answer("I couldn't find an answer to your question. Forwarding it to the operator. You'll receive a response as soon as possible!", reply_to_message_id=message.message_id)
            else:
                await message.answer("There was an error processing your request. Please try again later.", reply_to_message_id=message.message_id)


async def get_new_answers():
    while True:
        await asyncio.sleep(5)
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8000/answers', params={}) as response:
                if response.status == 200:
                    data = await response.json()

                    for answer in data:
                        qid = answer['id']
                        answer = answer['a']
                        # send the answer to the user
                        
                        await bot.send_message(answer['user_id'], answer['answer'], reply_to_message_id=answer['message_id'])
                        await session.delete(f"http://localhost:8000/answers/{qid}")
                else:
                    pass

async def main():
    asyncio.create_task(get_new_answers())
    await dp.start_polling(bot, skip_updates=True)
    

if __name__ == '__main__':
    asyncio.run(main())
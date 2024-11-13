from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import random
import asyncio


bot = Bot(token="7844671961:AAHhE0Uuz4u7Ge00as21A4AqG-TFotrRWcQ")
dp = Dispatcher(storage=MemoryStorage())

async def send_otp(user_id: int):
    try:
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        await bot.send_message(user_id, otp)
        return otp
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello! I'm your registration bot.")

async def start_bot() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())
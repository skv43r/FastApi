from aiogram import Dispatcher, types
from aiogram.filters import Command

def register_handlers(dp: Dispatcher):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer("Hello! I'm your registration bot.")
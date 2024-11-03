from dotenv import load_dotenv
from os import getenv
from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters import BaseFilter
from aiogram.client.bot import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from messages import TEXT_B_VIEW_SCHEDULE
from keyboards.button import main_kb, check_subscription_kb

load_dotenv()

router = Router()

admin_username: list[str] = [getenv('ADMIN_USERNAME'), getenv('WITCH_USERNAME')]
@router.message(F.text == TEXT_B_VIEW_SCHEDULE)
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    with open(getenv('CSHEDULE'), "r", encoding="utf-8") as file:
        content = file.read()
    await message.answer(
        text=f"<pre>Ведьмин писаръ</pre> \n{content}", parse_mode=ParseMode.HTML,
        reply_markup=main_kb(message.from_user.username, admin_username)
    )
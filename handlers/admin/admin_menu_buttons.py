from dotenv import load_dotenv
from os import getenv

from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode

from messages import TEXT_B_ADMIN, TEXT_B_AWARDS_ACTION
from keyboards.button import admin_kb, award_actions_kb
from filters.is_admin import IsAdmin

load_dotenv()
admin_username: list[str] = [getenv('ADMIN_USERNAME'), getenv('WITCH_USERNAME')]

router = Router()
router.message.filter(IsAdmin(admin_username))

@router.message(F.text == TEXT_B_ADMIN)
async def cmd_display_awards(message: Message):
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nПриветствую тебя, {message.from_user.full_name}! Да будет светел твой путь!', parse_mode=ParseMode.HTML, reply_markup=admin_kb())

@router.message(F.text == TEXT_B_AWARDS_ACTION)
async def cmd_display_awards(message: Message):
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nО, благие деяния! Запишем, как будем щедры к тем, кто обрел успехи в своих трудах.', parse_mode=ParseMode.HTML, reply_markup=award_actions_kb())
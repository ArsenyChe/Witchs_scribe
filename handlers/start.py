from dotenv import load_dotenv
from os import getenv
from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters import BaseFilter
from aiogram.client.bot import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from messages import TEXT_START, TEXT_B_REMOVE, TEXT_SUBSCRIBE, TEXT_B_SUBSCRIBE
from keyboards.button import main_kb, check_subscription_kb

load_dotenv()

router = Router()

admin_username: list[str] = [getenv('ADMIN_USERNAME'), getenv('WITCH_USERNAME')]

@router.message(Command("start"))
async def cmd_start(message: Message, bot: Bot):
    user_channel_status = await bot.get_chat_member(chat_id= getenv('GROUP_MAIN'), user_id=message.from_user.id)

    if user_channel_status.status not in ['left','kicked']:
        await message.answer(f'<pre>Ведьмин писаръ</pre> \n{message.from_user.full_name}, '+ TEXT_START, parse_mode=ParseMode.HTML, reply_markup=main_kb(message.from_user.username, admin_username))
    else:
        await message.answer(f'<pre>Ведьмин писаръ</pre>\n'+ TEXT_SUBSCRIBE, parse_mode=ParseMode.HTML, reply_markup=check_subscription_kb())

    await message.delete()

@router.message(F.text == TEXT_B_SUBSCRIBE)
async def cmd_start_2(message: Message, bot: Bot):
    user_channel_status = await bot.get_chat_member(chat_id= getenv('GROUP_MAIN'), user_id=message.from_user.id)

    if user_channel_status.status not in ['left','kicked']:
        await message.answer(f'<pre>Ведьмин писаръ</pre> \n{message.from_user.full_name}, '+ TEXT_START, parse_mode=ParseMode.HTML, reply_markup=main_kb(message.from_user.username, admin_username))
    else:
        await message.answer(f'<pre>Ведьмин писаръ</pre>\n'+ TEXT_SUBSCRIBE, parse_mode=ParseMode.HTML, reply_markup=check_subscription_kb())

    await message.delete()

@router.message(F.text == TEXT_B_REMOVE)
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="<pre>Ведьмин писаръ</pre> \nДела ваши завершились, и вы возвратились к первоначальным началам.", parse_mode=ParseMode.HTML,
        reply_markup=main_kb(message.from_user.username, admin_username)
    )
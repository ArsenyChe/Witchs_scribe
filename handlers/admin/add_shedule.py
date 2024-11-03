from data import database
from datetime import datetime

from dotenv import load_dotenv
from os import getenv
from aiogram import Router, F
from aiogram.types import Message
from aiogram.client.bot import Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from messages import TEXT_B_ADD_SCHEDULE, TEXT_SUBSCRIBE, TEXT_B_CONFIRM
from keyboards.button import choice_kb, main_kb, admin_kb
from filters.allowed_content_type import AllowedContentType
from filters.is_admin import IsAdmin

load_dotenv()
admin_username: list[str] = [getenv('ADMIN_USERNAME'), getenv('WITCH_USERNAME')]
router = Router()
router.message.filter(IsAdmin(admin_username))

class AddShedule(StatesGroup):
    shedule = State()
    confirmation = State()

@router.message(F.text == TEXT_B_ADD_SCHEDULE)
async def cmd_add_shedule_1(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddShedule.shedule)
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nУра! Новое расписание во благо настало. Изложи же текст полного сообщения с расписанием.', parse_mode=ParseMode.HTML, 
                         reply_markup=choice_kb())
    
@router.message(AddShedule.shedule, AllowedContentType(['text']))
async def cmd_music_2(message: Message, state: FSMContext):
    await state.update_data(shedule = message.text)
    data = await state.get_data()
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nНеужто ты искренне желаешь уберечь сие расписание?', parse_mode=ParseMode.HTML,
                         reply_markup=choice_kb(True))
    
    await message.answer(f'<pre>Ведьмин писаръ</pre> \n{data["shedule"]}', parse_mode=ParseMode.HTML)

    await state.set_state(AddShedule.confirmation)
    
@router.message(F.text == TEXT_B_CONFIRM, AddShedule.confirmation)
async def cmd_add_shedule_3(message: Message, state: FSMContext, bot: Bot):
    user_channel_status = await bot.get_chat_member(chat_id= getenv('GROUP_MAIN'), user_id=message.from_user.id)

    if user_channel_status.status not in ['left','kicked']:
        await state.update_data(confirmation = message.text)
        data = await state.get_data()
        
        with open(getenv('CSHEDULE'), "w", encoding="utf-8") as file:
            file.write(data["shedule"])

        await message.answer(f'<pre>Ведьмин писаръ</pre> \nРасписание сие записано.', parse_mode=ParseMode.HTML,
                        reply_markup=admin_kb())
        await state.clear()
    else:
        await message.answer(f'<pre>Ведьмин писаръ</pre> \n' + TEXT_SUBSCRIBE, parse_mode=ParseMode.HTML, reply_markup=main_kb(message.from_user.username, admin_username))

    await state.clear()
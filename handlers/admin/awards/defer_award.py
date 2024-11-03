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

from messages import TEXT_B_DEFER_AWARDS, TEXT_SUBSCRIBE
from keyboards.button import choice_kb, main_kb,award_list_kb, award_actions_kb
from filters.allowed_content_type import AllowedContentType
from filters.is_int import IsInt
from filters.is_admin import IsAdmin

load_dotenv()
admin_username: list[str] = [getenv('ADMIN_USERNAME'), getenv('WITCH_USERNAME')]
router = Router()
router.message.filter(IsAdmin(admin_username))

class DeferAwards(StatesGroup):
    award_id = State()

@router.message(F.text == TEXT_B_DEFER_AWARDS)
async def cmd_defer_awards_1(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(DeferAwards.award_id)
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nДавайте снова откроем награду. Напиши номер её, что требует переоткрытия.', parse_mode=ParseMode.HTML, 
                         reply_markup=choice_kb())
    
@router.message(DeferAwards.award_id, AllowedContentType(['text']), IsInt())
async def cmd_defer_awards_2(message: Message, state: FSMContext, bot: Bot):
    user_channel_status = await bot.get_chat_member(chat_id= getenv('GROUP_MAIN'), user_id=message.from_user.id)

    if user_channel_status.status not in ['left','kicked']:
        await state.update_data(award_id = message.text)
        data = await state.get_data()
        await database.defer_award(int(data['award_id']))
        await message.answer(f'<pre>Ведьмин писаръ</pre> \nНаграда закрыта.', parse_mode=ParseMode.HTML,
                        reply_markup=award_actions_kb())
        await state.clear()
    else:
        await message.answer(f'<pre>Ведьмин писаръ</pre> \n' + TEXT_SUBSCRIBE, parse_mode=ParseMode.HTML, reply_markup=main_kb(message.from_user.username, admin_username))

    await state.clear()
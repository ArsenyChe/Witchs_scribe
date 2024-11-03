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

from messages import TEXT_B_ADD_AWARDS,TEXT_B_AWARDS_BOOK, TEXT_B_AWARDS_GAME,TEXT_B_AWARDS_VIEWING, TEXT_B_AWARDS_ARTICLE, TEXT_SUBSCRIBE, TEXT_B_CARD
from keyboards.button import choice_kb, main_kb,award_list_kb, award_actions_kb
from filters.allowed_content_type import AllowedContentType
from filters.is_admin import IsAdmin

load_dotenv()
admin_username: list[str] = [getenv('ADMIN_USERNAME'), getenv('WITCH_USERNAME')]
router = Router()
router.message.filter(IsAdmin(admin_username))

class AddAwards(StatesGroup):
    user_name = State()
    award_name = State()
    award = State()

@router.message(F.text == TEXT_B_ADD_AWARDS)
async def cmd_add_awards_1(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddAwards.user_name)
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nДавайте добавим новую награду для добродетельного человека. Напиши имя молодца!', parse_mode=ParseMode.HTML, 
                         reply_markup=choice_kb())
    
@router.message(AddAwards.user_name, AllowedContentType(['text']))
async def cmd_add_awards_2(message: Message, state: FSMContext):
    await state.update_data(user_name = message.text)
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nНапиши же название награды из списка.', parse_mode=ParseMode.HTML,
                         reply_markup=award_list_kb())

    await state.set_state(AddAwards.award_name)

@router.message(AddAwards.award_name, F.text.in_([TEXT_B_AWARDS_BOOK, TEXT_B_AWARDS_GAME, TEXT_B_AWARDS_VIEWING, TEXT_B_AWARDS_ARTICLE, TEXT_B_CARD]))
async def cmd_add_awards_3(message: Message, state: FSMContext, bot: Bot):
    user_channel_status = await bot.get_chat_member(chat_id= getenv('GROUP_MAIN'), user_id=message.from_user.id)
    if user_channel_status.status not in ['left','kicked']:
        await state.update_data(award_name = message.text)
        if message.text in [TEXT_B_AWARDS_ARTICLE, TEXT_B_CARD]:
            data = await state.get_data()
            await database.add_award(data["user_name"], data["award_name"], "", False , datetime.now().strftime("%Y-%m-%d, %H:%M"))
            await message.answer(f'<pre>Ведьмин писаръ</pre> \nНаграда "{data["award_name"]}" для {data["user_name"]}', parse_mode=ParseMode.HTML, reply_markup=award_actions_kb())

            await state.clear()
        else:
            await message.answer(f'<pre>Ведьмин писаръ</pre> \nУкажи название заказа.', parse_mode=ParseMode.HTML,
                            reply_markup=choice_kb())
            await state.set_state(AddAwards.award)
    else:
        await message.answer(f'<pre>Ведьмин писаръ</pre> \n' + TEXT_SUBSCRIBE, parse_mode=ParseMode.HTML, reply_markup=main_kb(message.from_user.username, admin_username))
        await state.clear()


@router.message(AddAwards.award, AllowedContentType(['text']))
async def cmd_add_awards_4(message: Message, state: FSMContext, bot: Bot):
    user_channel_status = await bot.get_chat_member(chat_id= getenv('GROUP_MAIN'), user_id=message.from_user.id)
    if user_channel_status.status not in ['left','kicked']:
        await state.update_data(award = message.text)
        data = await state.get_data()

        await database.add_award(data["user_name"], data["award_name"], data["award"], False , datetime.now().strftime("%Y-%m-%d, %H:%M"))
        await message.answer(f'Награда "{data["award_name"]}" с сообщением "{data["award"]} для {data["user_name"]}', reply_markup=award_actions_kb())
    else:
        await message.answer(f'<pre>Ведьмин писаръ</pre> \n' + TEXT_SUBSCRIBE, parse_mode=ParseMode.HTML, reply_markup=main_kb(message.from_user.username, admin_username))

    await state.clear()
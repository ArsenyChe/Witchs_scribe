from dotenv import load_dotenv
from os import getenv
from aiogram import Router, F
from aiogram.types import Message
from aiogram.client.bot import Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from messages import TEXT_B_EVENT, TEXT_B_CONFIRM, TEXT_SUBSCRIBE, TEXT_RESTART_WARNING
from keyboards.button import choice_kb, main_kb
from filters.allowed_content_type import AllowedContentType


load_dotenv()
router = Router()
admin_username: list[str] = [getenv('ADMIN_USERNAME'), getenv('WITCH_USERNAME')]

class SendEvent(StatesGroup):
    music = State()
    massage = State()
    confirmation = State()
    
@router.message(F.text == TEXT_B_EVENT)
async def cmd_music_1(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(SendEvent.music)
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nЕсли сердцу твоему угодно, предложи мелодию для концерта, который пройдет 01.12.2024. \nМелодия сия должна быть: \n1) на языке иностранном, дабы волшебница могла её переделать по своему усмотрению; \n2) некрепко вокальная, дабы лесная ведьма сумела её поэтично перевести и спеть во время сего концерта.\n\nДабы вознести мелодию, укажите ссылку на сию композицию.\n\n{TEXT_RESTART_WARNING}', parse_mode=ParseMode.HTML, 
                         reply_markup=choice_kb())
    
@router.message(SendEvent.music, AllowedContentType(['text']))
async def cmd_music_2(message: Message, state: FSMContext):
    await state.update_data(music = message.text)
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nПриложите комментарии к сей композиции, дабы мы могли внять вашим мыслям и чувствам, порожденным ею.', parse_mode=ParseMode.HTML,
                         reply_markup=choice_kb())

    await state.set_state(SendEvent.massage)

@router.message(SendEvent.massage, AllowedContentType(['text']))
async def cmd_music_3(message: Message, state: FSMContext):
    await state.update_data(massage = message.text)
    data = await state.get_data()
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nЖелаете ли вы вознести сие слово в святой канал "Музыка для концерта"? Пожалуйста, укажите одну из избранных команд из списка.', parse_mode=ParseMode.HTML,
                         reply_markup=choice_kb(True))

    await message.answer(f'{data["music"]} \n{data["massage"]} \n\n🌼{message.from_user.full_name}🌼')

    await state.set_state(SendEvent.confirmation)

@router.message(F.text == TEXT_B_CONFIRM, SendEvent.confirmation)
async def cmd_music_4(message: Message, state: FSMContext, bot: Bot):
    user_channel_status = await bot.get_chat_member(chat_id= getenv('GROUP_MAIN'), user_id=message.from_user.id)

    if user_channel_status.status not in ['left','kicked']:
        await state.set_state(SendEvent.confirmation)
        data = await state.get_data()
        await bot.send_message(getenv('GROUP_EVENT'), f'{data["music"]} \n{data["massage"]} \n\n🌼{message.from_user.full_name}🌼')

        await message.answer(f'<pre>Ведьмин писаръ</pre> \nСлово ваше с любовью вознесено в канал "Музыка для концерта".', parse_mode=ParseMode.HTML, reply_markup=main_kb(message.from_user.username, admin_username))
    else:
        await message.answer(f'<pre>Ведьмин писаръ</pre> \n'+ TEXT_SUBSCRIBE, parse_mode=ParseMode.HTML, reply_markup=main_kb(message.from_user.username, admin_username))

    await state.clear()
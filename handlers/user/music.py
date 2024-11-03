from dotenv import load_dotenv
from os import getenv
from aiogram import Router, F
from aiogram.types import Message
from aiogram.client.bot import Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from messages import TEXT_B_MUSIC, TEXT_B_CONFIRM, TEXT_SUBSCRIBE, TEXT_RESTART_WARNING
from keyboards.button import choice_kb, main_kb
from filters.allowed_content_type import AllowedContentType


load_dotenv()
router = Router()
admin_username: list[str] = [getenv('ADMIN_USERNAME'), getenv('WITCH_USERNAME')]

class SendMusic(StatesGroup):
    music = State()
    massage = State()
    confirmation = State()
    
@router.message(F.text == TEXT_B_MUSIC)
async def cmd_music_1(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(SendMusic.music)
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nЕсли сердцу твоему угодно, вознеси мелодию, что радует душу до небес.\n\nДабы вознести мелодию на святое место "Мелодии-души", укажите ссылку на сию композицию.\n\n{TEXT_RESTART_WARNING}', parse_mode=ParseMode.HTML, 
                         reply_markup=choice_kb())
    
@router.message(SendMusic.music, AllowedContentType(['text']))
async def cmd_music_2(message: Message, state: FSMContext):
    await state.update_data(music = message.text)
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nПриложите комментарии к сей композиции, дабы мы могли внять вашим мыслям и чувствам, порожденным ею.', parse_mode=ParseMode.HTML,
                         reply_markup=choice_kb())

    await state.set_state(SendMusic.massage)

@router.message(SendMusic.massage, AllowedContentType(['text']))
async def cmd_music_3(message: Message, state: FSMContext):
    await state.update_data(massage = message.text)
    data = await state.get_data()
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nЖелаете ли вы вознести сие слово в святой канал "Мелодии души"? Пожалуйста, укажите одну из избранных команд из списка.', parse_mode=ParseMode.HTML,
                         reply_markup=choice_kb(True))

    await message.answer(f'{data["music"]} \n{data["massage"]} \n\n🌼{message.from_user.full_name}🌼')

    await state.set_state(SendMusic.confirmation)

@router.message(F.text == TEXT_B_CONFIRM, SendMusic.confirmation)
async def cmd_music_4(message: Message, state: FSMContext, bot: Bot):
    user_channel_status = await bot.get_chat_member(chat_id= getenv('GROUP_MAIN'), user_id=message.from_user.id)

    if user_channel_status.status not in ['left','kicked']:
        await state.set_state(SendMusic.confirmation)
        data = await state.get_data()
        await bot.send_message(getenv('GROUP_MUSIC'), f'{data["music"]} \n{data["massage"]} \n\n🌼{message.from_user.full_name}🌼')

        await message.answer(f'<pre>Ведьмин писаръ</pre> \nСлово ваше с любовью вознесено в канал "Мелодии души".', parse_mode=ParseMode.HTML, reply_markup=main_kb(message.from_user.username, admin_username))
    else:
        await message.answer(f'<pre>Ведьмин писаръ</pre> \n'+ TEXT_SUBSCRIBE, parse_mode=ParseMode.HTML, reply_markup=main_kb(message.from_user.username, admin_username))

    await state.clear()
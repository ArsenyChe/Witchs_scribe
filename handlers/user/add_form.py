from dotenv import load_dotenv
from os import getenv
from aiogram import Router, F
from aiogram.types import Message
from aiogram.client.bot import Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder

from messages import TEXT_B_FORM, TEXT_B_CONFIRM,TEXT_SUBSCRIBE, TEXT_RESTART_WARNING
from keyboards.button import choice_kb, main_kb,award_list_kb, award_actions_kb
from filters.allowed_content_type import AllowedContentType

load_dotenv()
router = Router()
admin_username: list[str] = [getenv('ADMIN_USERNAME'), getenv('WITCH_USERNAME')]

class AddForm(StatesGroup):
    form = State()
    picture = State()
    confirmation = State()

@router.message(F.text == TEXT_B_FORM)
async def cmd_add_form_1(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddForm.form)
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nО, новая записка! Для наполнения анкеты, вам надобно будет ответить на двадцать вопросцов и явить рисунок кота по имени Сириус. \n\nУмоляю, ответьте на вопросцы ниже. Ответ свой изложите текстом.\n\n{TEXT_RESTART_WARNING}', parse_mode=ParseMode.HTML, 
                         reply_markup=choice_kb())
    await message.answer(f'''<pre>Ведьмин писаръ</pre> \n
1. Твоё имя/никъ? 
2. Сколько тебе летъ?
3. Твой знак зодиака?
4. Откуда ты родомс?
5. Твои любимые магические цвета?
6. С чем больше всего любишь пить чай/кофе/настоечку/пиво?
7. Твои любимые книги/фильмы/сериалы, которые произвели на тебя неизгладимое волшебное впечатление?
8. У тебя есть братья/сестры/кармические родители/древние боги-бабушки/дедушки среди стримеров?
9. Чем ты занимаешься в свободное от стримов время?
10. Твои любимые втурберы/втуберши?
11. Твои любимые мемы/алерты?
12. У тебя есть домашние/лесные животные?
13. Что/кто тебя вдохновляетъ?
14. Твоё любимое время года/день недели/фаза луны/часть сутокъ?
15. Твой любимые прозвища Госпожи-колдуньи?
16. С кем ты дружишь/ведешь чаровную переписку из чатика?
17. Как распознать Болотную Кикимору?
18. Напиши пожелание Хозяйке анкеты Албиэль.
19. Нарисуй Сириуса.
20. Чего бы ты хотел видеть больше на канале?''', parse_mode=ParseMode.HTML)
    
@router.message(AddForm.form, AllowedContentType(['text']))
async def cmd_add_form_2(message: Message, state: FSMContext):

    await state.update_data(form = message.text)
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nПриложи же изображение кота по имени Сириус, и сие совершенно необходимо.', parse_mode=ParseMode.HTML,
                         reply_markup=choice_kb())

    await state.set_state(AddForm.picture)

@router.message(AddForm.picture, AllowedContentType(['photo']))
async def cmd_music_3(message: Message, state: FSMContext):
    await state.update_data(picture=message.photo[-1].file_id)
    data = await state.get_data()
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nЖелаете ли вы вознести сие слово в святой канал "Кудесная анкета дружбы"? Пожалуйста, укажите одну из избранных команд из списка.', parse_mode=ParseMode.HTML,
                         reply_markup=choice_kb(True))

    await message.answer_photo(photo=data["picture"], caption=f'{data["form"]} \n\nАнкета от {message.from_user.full_name}')

    await state.set_state(AddForm.confirmation)

@router.message(F.text == TEXT_B_CONFIRM, AddForm.confirmation)
async def cmd_add_form_4(message:Message,state:FSMContext, bot: Bot):
    await state.update_data(confirmation=message.text)
    data = await state.get_data()
    user_channel_status = await bot.get_chat_member(chat_id= getenv('GROUP_MAIN'), user_id=message.from_user.id)

    if user_channel_status.status not in ['left','kicked']:
        await bot.send_photo(getenv('GROUP_FORM'),photo=data["picture"], caption=f'{data["form"]} \n\nАнкета от {message.from_user.full_name}', reply_markup=main_kb(message.from_user.username, admin_username))
    else:
        await message.answer(f'<pre>Ведьмин писаръ</pre> \n' + TEXT_SUBSCRIBE, parse_mode=ParseMode.HTML, reply_markup=main_kb(message.from_user.username, admin_username))
    
    await state.clear()
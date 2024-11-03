from dotenv import load_dotenv
from os import getenv
from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode

from messages import TEXT_B_VIEW_EVENT_2
from keyboards.button import main_kb


load_dotenv()
router = Router()
admin_username: list[str] = [getenv('ADMIN_USERNAME'), getenv('WITCH_USERNAME')]
    
@router.message(F.text == TEXT_B_VIEW_EVENT_2)
async def cmd_view_event(message: Message):
    await message.answer(f'<pre>Ведьмин писаръ</pre> \nСуть ВедьМЯбря заключается в том, что в течении всего ноября в определенные дни мы с вами будет смотреть, али играть, али читать, али делать что-то ручками против того или иного вида нечисти! \nИнтересно? Тогда присоединяйтесь к Ведунье в борьбе с злыднями!🪄🪄🪄', parse_mode=ParseMode.HTML, 
                         reply_markup=main_kb(message.from_user.username, admin_username))
    photo = FSInputFile(getenv('TIMETABLE_PICTURE_PATH'))
    await message.answer_photo(photo)
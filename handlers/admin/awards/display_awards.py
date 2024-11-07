from data import database

from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from messages import TEXT_B_AWARDS

router = Router()

@router.message(F.text == TEXT_B_AWARDS)
async def cmd_display_awards(message: Message):
    awards = await database.display_awards()
    response = "<pre>Ведьмин писаръ</pre> \nПеред вами свиток, где записаны просьбы душ, жаждущих помощи и заботы. \n"
    check_award = None

    for award in awards:
        if award[2] != check_award:
            if response: 
                await message.answer(response, parse_mode=ParseMode.HTML)
                response = ""
            response += f'<pre>🍂 {award[2]}</pre>\n'
            check_award = award[2]

        if award[5] != "":
            response += f'<pre>{award[0]}) {award[1]} изъявил(а) желание получить награду, нареченную "{award[2]}", именем "{award[5].strip()}" \nВремя сие: {award[4]}, Состояние: 🎃</pre>\n'
        else:
            response += f'<pre>{award[0]}) {award[1]} изъявил(а) желание получить награду, нареченную "{award[2]}" \nВремя сие: {award[4]}, Состояние: 🎃</pre>\n'

    if response:
        await message.answer(response, parse_mode=ParseMode.HTML)
    
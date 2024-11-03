from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.enums import ParseMode

class IsInt(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        try:
            int(message.text)
            return True
        except ValueError:
            await message.answer("<pre>Ведьмин писаръ</pre>Возьми к сведению указанный выше разрешённый вид посланий. Исполни повеление, следуя данной инструкции.", parse_mode=ParseMode.HTML)
            return False
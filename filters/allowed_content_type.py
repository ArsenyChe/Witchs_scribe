from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.enums import ParseMode

class AllowedContentType(BaseFilter):
    def __init__(self, content_type: list[str]) -> None:
        self.content_type = content_type

    async def __call__(self, message: Message) -> bool:
        if message.content_type not in self.content_type: await message.answer("<pre>Ведьмин писаръ</pre>Возьми к сведению указанный выше разрешённый вид посланий. Исполни повеление, следуя данной инструкции.", parse_mode=ParseMode.HTML)
        return message.content_type in self.content_type
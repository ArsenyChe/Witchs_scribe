from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAdmin(BaseFilter):
    def __init__(self, admin_username: list[str]) -> None:
        self.admin_username = admin_username

    async def __call__(self, message: Message) -> bool:
        return message.from_user.username in self.admin_username
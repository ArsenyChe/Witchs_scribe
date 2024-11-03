import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import start
from handlers.admin.awards import add_award, display_awards, fulfill_award, defer_award
from handlers.user import add_form, music, needlework, event, view_schedule, event_2
from handlers.admin import admin_menu_buttons, add_shedule

async def main():
    load_dotenv()
    bot = Bot(getenv('TOKEN_API'))

    dp = Dispatcher()
    dp.include_routers(start.router, music.router, display_awards.router, admin_menu_buttons.router, add_award.router, fulfill_award.router, defer_award.router, add_form.router, event.router, view_schedule.router,add_shedule.router, event_2.router)
    print(f'[INFO] Bot connect')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e: 
        print(f'[INFO] Bot run {e}')
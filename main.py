import asyncio
import traceback
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN, ADMIN_ID
from tugmachalar import set_commands
from logger import log_system
from handlers import router as handlers_router   # handlers.py dagi router
from obuna import router as obuna_router         # obuna.py dagi router


async def main():
    print("Bot ishga tushdi...")
    log_system("Bot ishga tushdi ✅")

    bot = None
    try:
        bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp = Dispatcher()

        # Buyruqlarni o‘rnatish
        await set_commands(bot)

        # Adminni ogohlantirish
        try:
            await bot.send_message(chat_id=ADMIN_ID, text="Bot ishga tushdi ✅")
        except Exception as ex:
            log_system(f"Adminni ogohlantirishda xatolik: {ex}", level="error")

        # Routerni ulash (obuna birinchi bo‘lishi kerak!)
        dp.include_router(obuna_router)       # obuna.py
        dp.include_router(handlers_router)    # handlers.py

        # Pollingni ishga tushirish
        await dp.start_polling(bot)

    except Exception as e:
        log_system(f"Xatolik: {e}\nTraceback:\n{traceback.format_exc()}", level="error")
        if bot:
            try:
                await bot.send_message(chat_id=ADMIN_ID, text=f"Xatolik yuz berdi: {e}")
            except Exception as ex:
                log_system(f"Adminga xabar yuborishda xatolik: {ex}", level="error")

    finally:
        log_system("Bot to‘xtadi ❌")
        if bot:
            try:
                await bot.send_message(chat_id=ADMIN_ID, text="Bot to‘xtadi ❌")
            except Exception as ex:
                log_system(f"Adminga xabar yuborishda xatolik: {ex}", level="error")


if __name__ == "__main__":
    asyncio.run(main())

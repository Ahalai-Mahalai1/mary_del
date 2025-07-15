import asyncio
from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from handlers import other, handlers
from aiogram import types
# Функция конфигурирования и запуска бота
async def main() -> None:

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.bot.token)
    dp = Dispatcher()
    dp.include_router(handlers.router)
    dp.include_router(other.router)
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    #await reply_markup = types.ReplyKeyboardRemove()

    await dp.start_polling(bot)


asyncio.run(main())
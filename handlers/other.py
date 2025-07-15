from aiogram import Bot, Router
from aiogram.types import Message
from config.config import Config, load_config
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
config: Config = load_config()
bot = Bot(
    token=config.bot.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
user_id = 406802660
router = Router()
# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команд "/start" и "/help"
@router.message()
async def send_echo(message: Message):
    try:
        user = message.from_user
        await bot.send_message(user_id,f"User {user.full_name} — ID: {user.id}")
        await message.send_copy(chat_id=message.chat.id)

    except TypeError:
        await message.reply(text='Данный тип апдейтов не поддерживается')
import asyncio
from random import randint
import os
from config.config import Config, load_config
from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
router = Router()
config: Config = load_config()
bot = Bot(token=config.bot.token)
lst=[]
# Cоздаем класс StatesGroup для нашей машины состояний
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    wait_text = State()        # Состояние ожидания ввода имени
    wait_time = State()         # Состояние ожидания ввода возраста
# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(),StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='''Этот бот удаляет пользователей по id из канала через выбранные промежутки времени''')
# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне машины состояний\n\n'
             'Чтобы начать процесс удаления - '
             'отправьте команду /kick_id'
    )
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из процесса удаления\n\n'
             'Чтобы снова начать процесс удаления - '
             'отправьте команду /kick_id'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()

# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='''Этот бот удаляет пользователей по id из канала через выбранные промежутки времени''')
@router.message(Command(commands='kick_id'), StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(text='''Отправьте текстовый файл''')
    await state.set_state(FSMFillForm.wait_text)
@router.message(StateFilter(FSMFillForm.wait_text), F.document)
async def process_name_sent(message: Message, state: FSMContext):
    global lst
    document = message.document
    file = await bot.get_file(document.file_id)
    file_path = file.file_path
    local_path = f"./{document.file_name}"
    await bot.download_file(file_path, destination=local_path)
    with open(local_path, "r", encoding="utf-8") as f:
        text = f.read()
    lst=text.split('\n')
    if os.path.exists(local_path):
          os.remove(local_path)
    await message.answer(text='Спасибо!\n\nА теперь введите через сколько должны удаляться пользователи в секундах')
    # # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.wait_time)
@router.message(StateFilter(FSMFillForm.wait_text))
async def warning_not_text(message: Message):
    await message.answer(
        text='Это не файл'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )
@router.message(StateFilter(FSMFillForm.wait_time))
async def process_time_sent(message: Message, state: FSMContext):
    await message.answer(text='Спасибо!\n\nНачинаем удалять!')
    await asyncio.sleep(int(message.text))
    while lst:
        pos=randint(0,len(lst)-1)
        try:
            #await bot.ban_chat_member(chat_id="@thisisachanel080725", user_id=lst[pos])
            #await asyncio.sleep(1)  # можно сразу разбанить, чтобы можно было снова вступить
            #await bot.unban_chat_member(chat_id="@thisisachanel080725", user_id=lst[pos])
            await bot.send_message(chat_id=message.chat.id, text=f"Пользователь {lst[pos]} был удалён.")
        except Exception as e:
            await bot.send_message(chat_id=message.chat.id, text=f"Ошибка при удалении: {e}")
        znach=lst[pos]
        while znach in lst:
            lst.remove(znach)
        await asyncio.sleep(int(message.text))
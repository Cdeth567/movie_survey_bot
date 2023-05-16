# @B11_demo_bot
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token='6288021917:AAHgqNbuWdQxZzXyph3LU36f3n5E-mGYl3w', parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)


class Poll_film(StatesGroup):
    waiting_for_1 = State()
    waiting_for_2 = State()
    waiting_for_3 = State()
    waiting_for_4 = State()


poll = ['Драма', 'Исторический фильм',
        'Боевик', 'Приключенческий фильм',
        'Триллер', 'Детектив',
        'Комедия', 'Фантастика', 'Отмена']


kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(*poll)


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Привет. Какой жанр фильмов вам нравится?", reply_markup=kb)
    await Poll_film.waiting_for_1.set()


async def chosen_1(message: types.Message, state: FSMContext):
    if message.text not in poll:
        await message.answer("Пожалуйста, выберите ответ, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_11=message.text.lower())
    await Poll_film.next()
    await message.answer("Почему вам нравится этот жанр?")


async def chosen_2(message: types.Message, state: FSMContext):
    await state.update_data(chosen_21=message.text.lower())
    await Poll_film.next()
    await message.answer("Какой у вас любимый фильм?")


async def chosen_3(message: types.Message, state: FSMContext):
    await state.update_data(chosen_31=message.text.lower())
    await Poll_film.next()
    await message.answer("Дайте совет людям, которые смотрят слишком много фильмов")


async def chosen_4(message: types.Message, state: FSMContext):
    await state.update_data(chosen_41=message.text.lower())
    user_data = await state.get_data()
    await message.answer(f'РЕЗУЛЬТАТЫ ОПРОСА\n'
                         f'Любимый жанр: {user_data["chosen_11"]}\n'
                         f'Причина, по которой вам нравится этот жанр: "{user_data["chosen_21"]}"\n'
                         f'Любимый фильм: {user_data["chosen_31"]}\n'
                         f'Ваш совет: {user_data["chosen_41"]}')
    await state.finish()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(chosen_1, state=Poll_film.waiting_for_1)
    dp.register_message_handler(chosen_2, state=Poll_film.waiting_for_2)
    dp.register_message_handler(chosen_3, state=Poll_film.waiting_for_3)
    dp.register_message_handler(chosen_4, state=Poll_film.waiting_for_4)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")


async def main():
    register_handlers_common(dp)
    register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

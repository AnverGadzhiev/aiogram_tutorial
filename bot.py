#!venv/bin/python
from aiogram.utils.exceptions import BotBlocked
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types

# Объект бота
bot_token = open('bot_info.txt').readline()
bot = Bot(token=f'{bot_token}')
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

message_quantity = 0

# Хэндлер на команду /test1
@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    global message_quantity
    message_quantity += 1
    # await message.reply(f'I got {message_quantity} messages')
    await message.reply(f'{message_quantity}')

@dp.message_handler(commands="block")
async def cmd_block(message: types.Message):
    await asyncio.sleep(10.0)  # Здоровый сон на 10 секунд
    await message.reply("Вы заблокированы")

@dp.message_handler(content_types=[types.ContentType.STICKER])
async def echo_document(message: types.Message):
    await message.reply_sticker(message.sticker.file_id)



@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

# - *- coding: utf- 8 - *-
import config
import logging
import random
import sys
from importlib import reload
reload(sys)
from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter



# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')

# відкриття файлу та рандомне вибрання
def parse_text_db():
	with open('test/endokrynka/' + str(random.randint(1, 90)) + '.txt', mode='r', encoding='utf-8') as f:
		homework = f.read()
	return homework
# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, True)
	
	await message.answer("Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")

# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
        
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")

# keyboard
item1 = types.KeyboardButton('🎲 Рандомне питання')

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(item1)

# добавляємо кнопки
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!", reply_markup=markup)

# Кнопка " Рандомне питання"
@dp.message_handler(lambda message: message.text == "🎲 Рандомне питання")
async def random_btn(message: types.Message):
    await message.answer(parse_text_db(), parse_mode='html')

# запускаем лонг поллинг
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
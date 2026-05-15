import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
# API Kalitlar
BOT_TOKEN = '8288618524:AAE9M1ymkuUUUx6dgSjn31UPL7yit_sKH38'
WEATHER_API_KEY = 'b25f123a5ab52292a628cc5a26df2450'
CURRENCY_API = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"

# Botni sozlash
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# 1. ASOSIY MENYU
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    buttons = [
        [types.KeyboardButton(text="🇺🇸 Dollar kursi")],
        [types.KeyboardButton(text="🌤 Ob-havo")],
        [types.KeyboardButton(text="📝 Tarjimon (Yo'riqnoma)")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.reply("Assalomu alaykum! Men ko'p funksiyali botman. Kerakli bo'limni tanlang:",
                        reply_markup=keyboard)


# 2. VALYUTA KURSI
@dp.message_handler(lambda message: message.text == "🇺🇸 Dollar kursi")
async def get_currency(message: types.Message):
    response = requests.get(CURRENCY_API).json()
    for item in response:
        if item['Ccy'] == 'USD':
            rate = item['Rate']
            date = item['Date']
            await message.answer(f"Bugungi dollar kursi: {rate} so'm\nSana: {date}")


 # 3. OB-HAVO (Shahar nomi orqali)
@dp.message_handler(lambda message: message.text == "🌤 Ob-havo")
async def ask_city(message: types.Message):
    await message.answer("Shahar nomini kiriting (Masalan: Toshkent):")


@dp.message_handler(lambda message: "havo" not in message.text.lower() and len(message.text) < 20)
async def get_weather(message: types.Message):
    city = message.text
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=uz"

    res = requests.get(url).json()
    if res.get("cod") != "404":
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        await message.answer(f"📍 {city} shahrida bugun: {desc}\nHarorat: {temp}°C")
    else:
        # Agar shahar topilmasa, tarjima deb qabul qilamiz (pastga o'tadi)
        pass


# 4. TARJIMON
@dp.message_handler()
async def translate_text(message: types.Message):
    # Agar bu shahar nomi bo'lmasa, tarjima qilamiz
    text_to_translate = message.text
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=uz&dt=t&q={text_to_translate}"

    try:
        res = requests.get(url).json()
        translated = res[0][0][0]
        await message.answer(f"🤖 Tarjima (O'zbekcha): \n\n{translated}")
    except:
        await message.answer("Xatolik yuz berdi yoki noto'g'ri buyruq.")


async def main():
    # Bot ishga tushishini boshlash
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot o'chirildi")
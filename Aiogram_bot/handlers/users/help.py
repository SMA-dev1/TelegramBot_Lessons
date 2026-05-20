import aiohttp

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from deep_translator import GoogleTranslator

API_KEY = 'ad44fee456d6a1d090bd4842'


router = Router()


@router.message(Command('help'))
async def bot_help(message: Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
            "/translate - Tarjima qilish (masalan: /translate salom)",
            "/dollar - Dollar kursi",
            "/ob_havo - Ob-havo holati",
            )
    await message.answer(text="\n".join(text))


@router.message(Command("translate"))
async def tarjima_handler(message: Message) -> None:
    # Buyruq nomini olib, qolgan matnni olish
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip():
        await message.answer(" 🙂 Tarjima uchun matn kiriting:\n/translate salom")
        return
    matn = args[1].strip()
    result = GoogleTranslator(source='uz', target='en').translate(matn)
    await message.answer(f"🔝 Tarjima: {result}")


@router.message(Command("dollar"))
async def dollar_handler(message: Message) -> None:
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/USD/UZS"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            kurs = data['conversion_rate']
    await message.answer(f" Dollar kursi: {kurs} UZS")


@router.message(Command("ob_havo"))
async def havo_handler(message: Message) -> None:
    url = "https://wttr.in/Urgench?format=j1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json(content_type=None)
            temp = data['current_condition'][0]['temp_C']
            feels = data['current_condition'][0]['FeelsLikeC']
            desc = data['current_condition'][0]['weatherDesc'][0]['value']
    await message.answer(
        f"😊 Urgench ob-havo:\n"
        f" 🔝 Harorat: {temp}°C\n"
        f" 🤩 His qilinishi: {feels}°C\n"
        f"👍 Holat: {desc}"
    )

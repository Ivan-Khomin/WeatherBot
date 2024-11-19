from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineQuery
from aiogram.filters import Command, CommandStart

import app.keyboards as kb
from app.weather import Weather

router = Router()

url = 'https://ua.sinoptik.ua/погода-суми/10-днів'
weather = Weather(url)
html = weather.get_html()
city = ''


@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer(f"Привіт, {message.from_user.first_name}!\n"
                         f"Хочеш дізнатися про погоду? Натисни /weather.")


@router.message(Command('help'))
async def help_message(message: Message):
    await message.answer("/start - почати роботу бота\n"
                         "/help - допомога\n"
                         "/weather - показати прогноз погоди")


@router.message(Command('weather'))
async def weather_message(message: Message):
    await message.answer("Виберіть місто", reply_markup=kb.keyboard_citys)


@router.message(F.text)
async def handle_city(message: Message):
    global city
    global html
    city = message.text.lower()
    await message.answer(f"Ви хочете дізнатися прогноз погоди в місті {city.title()}.\n"
                         f"Виберіть дні:",
                         reply_markup=kb.keyboard_days)
    url = f'https://ua.sinoptik.ua/погода-{city}/10-днів'
    weather.set_url(url)
    html = weather.get_html()


@router.callback_query(F.data.startswith('day-'))
async def weather_callback(callback_query: CallbackQuery):
    days = int(callback_query.data[4:])
    weather_list = weather.parse_weather(days)
    await callback_query.answer()
    if days == 1:
        await callback_query.message.answer(f"Погода в місті {city.title()}:\n{weather.print_weather()}")
    else:
        for text in weather_list:
            await callback_query.message.answer(text)


@router.inline_query()
async def weather_inline(inline_query: InlineQuery):
    global html, city, url
    city = inline_query.query.lower()
    url = f'https://ua.sinoptik.ua/погода-{city}/10-днів'
    weather.set_url(url)
    html = weather.get_html()
    await inline_query.answer(weather.print_weather_inline(inline_query, city))

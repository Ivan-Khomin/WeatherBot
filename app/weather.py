from bs4 import BeautifulSoup
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQuery
import requests


class Weather:
    url: str
    html: BeautifulSoup

    def __init__(self, url):
        self.url = url

    def get_html(self):
        response = requests.get(self.url)
        self.html = BeautifulSoup(response.content, 'html.parser')
        return self.html

    def set_url(self, url):
        self.url = url

    def parse_weather(self, days=10):
        result = []
        for i in range(1, days + 1):
            for element in self.html.select(f'#bd{i}.main'):
                day_week = element.select('.day-link')[0].text
                date = element.select('.date')[0].text
                month = element.select('.month')[0].text
                t_min = element.select('.temperature .min')[0].text
                t_max = element.select('.temperature .max')[0].text
                result.append(f"{day_week}\n"
                              f"{date} {month}\n\n"
                              f"{t_min}\n"
                              f"{t_max}")
        return result

    def parse_description(self):
        result = []
        for element in self.html.select('#bd1c.Tab'):
            description = element.select('.wDescription.clearfix .rSide .description')[0].text
            result.append(description)
        return result

    def parse_name(self):
        result = ''
        for element in self.html.select('#header.clearfix .cityName.cityNameShort'):
            name = element.find_all('h1')[0].text
            result = name
        return result

    def print_weather(self):
        res_weather = ''
        res_description = ''
        for i in self.parse_weather(1):
            res_weather = i
        for j in self.parse_description():
            res_description = j
        return f"{res_weather}\n\n-{res_description}"

    def print_weather_inline(self, inline_query: InlineQuery, city: str):
        result = []
        text = self.print_weather()
        if inline_query.query:
            result.append(InlineQueryResultArticle(
                id=self.parse_name(),
                title=self.parse_name(),
                input_message_content=InputTextMessageContent(
                    message_text=f"Погода в місті {city.title()}:\n{text}"
                ),
                description=self.parse_name(),
                thumbnail_width=48,
                thumbnail_height=48
            ))
            return result
        else:
            result.append(InlineQueryResultArticle(
                id='Error',
                title='Помилка',
                input_message_content=InputTextMessageContent(
                    message_text='Такого міста немає!'
                ),
                description='Такого міста немає!',
                thumbnail_width=48,
                thumbnail_height=48
            ))
            return result

import random
import sys
from bs4 import BeautifulSoup
import fake_useragent
import requests
import telebot
import json
import settings

user=fake_useragent.UserAgent.random
header= {'user-agent':'user'}
link=settings.LINK

token=settings.API_KEY
bot=telebot.TeleBot(token)
id_chanel=settings.ID_CHANEL

emoji_word = {
    'McGregor':'☘️',
    'Poirier' : '💎',
    'Jones' : '🦴',
}

random_emoji = ('💪🏼','👉🏼','💥','🔥','🏆','🚀','🎙','📌','📍','📩','❕','📣','💬')


respons=requests.get(link, headers=header).text

soup = BeautifulSoup(respons, 'html.parser')

# Извлечение ссылки
link = soup.find('a', class_='post__title')['href']

# Извлечение заголовка
title = soup.find('a', class_='post__title').get_text(strip=True)

print(f'Ссылка: {link}')
print(f'Заголовок: {title}')

current_link_title= {'link':link,'title':title}

def write_into_file(current_link_title):
    with open('data_new.txt', 'w',encoding='utf-8') as outfile:
        json.dump(current_link_title,outfile,indent=3)

def get_emoji():
    for key in title.split():
        if key in emoji_word:
            return emoji_word[key]
        else:
            return random.choice(random_emoji)


with open('data_new.txt') as json_file:
    old_link_title = json.load(json_file)

    if current_link_title != old_link_title:

        new_link = f'🔎 <a href="{current_link_title['link']}">Check Link</a>'

        text = f'{get_emoji()} {current_link_title['title']}{'\n\n'}{new_link}'

        bot.send_message(id_chanel, text,parse_mode='html')

        # Вызываю ф-цию для записи последней ссылки
        write_into_file(current_link_title)
    else:
        print('no new')

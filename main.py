import os
import uuid
import requests
import telebot
from urllib.parse import urlparse
from dotenv import load_dotenv
import re
load_dotenv()

TOKEN = os.getenv('TOKEN')
# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, send me your google map link plz")


@bot.message_handler()
def function_name(message):
    try:
        responses = requests.get(message.text)
        for response in responses.history:
            if '/maps?' in response.url: 
                parsedURL = urlparse(response.url)
                latlng = re.search("[0-9,.]{2,100}", parsedURL.query)
                latlng = latlng.group()
                latlng.replace(",", "%2C")

                finalURL = "https://www.waze.com/ul?ll=__LATLGN__&navigate=yes&zoom=17"
                finalURL = finalURL.replace("__LATLGN__", latlng)

                bot.send_message(message.chat.id, finalURL)
    except:
        bot.send_message(message.chat.id, 'Invalid URL')
        return

bot.polling()
import os
import requests
import telebot
import urllib.request
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
        gmapURL = re.search(
            "(?P<url>https?://[^\s]+)", message.text).group("url")
        responses = requests.get(gmapURL)

        if responses.history:
            for response in responses.history:
                with urllib.request.urlopen(response.url) as resp:
                    html = resp.read()
                    latlng = re.search(
                        "([0-9]\d[.][0-9]{7},[0-9]\d.[0-9]{7})", str(html))

                    if latlng:
                        latlng = latlng.group()
                        latlng = latlng.replace(",", "%2C")

                        finalURL = "https://www.waze.com/ul?ll=__LATLGN__&navigate=yes&zoom=17"
                        finalURL = finalURL.replace("__LATLGN__", latlng)

                        bot.send_message(message.chat.id, finalURL)
                        return
        else:
            latlng = re.search(
                "([0-9]\d[.][0-9]{7},[0-9]\d.[0-9]{7})", str(responses.content))
            if latlng:
                latlng = latlng.group()
                latlng = latlng.replace(",", "%2C")

                finalURL = "https://www.waze.com/ul?ll=__LATLGN__&navigate=yes&zoom=17"
                finalURL = finalURL.replace("__LATLGN__", latlng)

                bot.send_message(message.chat.id, finalURL)
                return

    except:
        bot.send_message(message.chat.id, 'Invalid URL 2')
        return


bot.polling()

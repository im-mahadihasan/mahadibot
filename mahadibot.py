import telebot
import requests
import schedule
import time
import threading
from bs4 import BeautifulSoup

bot = telebot.TeleBot("8827235553:AAFWoebzFW9k7tfCcml0tzTS15ExdknPL3k")
CHAT_ID = "6033189501"

# ===== অটো ফাংশন =====
def send_news():
    response = requests.get("https://news.ycombinator.com")
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = soup.find_all("span", class_="titleline", limit=5)
    result = "📰 সকালের খবর:\n\n"
    for i, h in enumerate(headlines, 1):
        result += str(i) + ". " + h.get_text() + "\n\n"
    bot.send_message(CHAT_ID, result)

def send_weather():
    response = requests.get("http://wttr.in/Feni?format=3")
    bot.send_message(CHAT_ID, "🌤️ সকালের আবহাওয়া:\n" + response.text)

# ===== কমান্ড =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """🤖 MahadiBot Pro তে স্বাগতম!

/weather — আবহাওয়া
/news — আজকের খবর
/country — দেশের তথ্য
/age — নামের গড় বয়স
/calc — calculator
/help — সাহায্য""")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, """📋 সাহায্য:

/weather — শহরের নাম দিন
/news — টপ ৫ খবর
/country — দেশের কোড দিন (BD, IN)
/age — নাম দিন
/calc — হিসাব লিখুন (যেমন: 5+3)""")

@bot.message_handler(commands=['weather'])
def weather(message):
    bot.reply_to(message, "কোন শহরের আবহাওয়া দেখবেন?")
    bot.register_next_step_handler(message, get_weather)

def get_weather(message):
    city = message.text
    response = requests.get("http://wttr.in/" + city + "?format=3")
    bot.reply_to(message, "🌤️ " + response.text)

@bot.message_handler(commands=['news'])
def news(message):
    bot.reply_to(message, "খবর আনছি... ⏳")
    send_news()

@bot.message_handler(commands=['country'])
def country(message):
    bot.reply_to(message, "দেশের কোড লিখুন (যেমন BD, IN, US):")
    bot.register_next_step_handler(message, get_country)

def get_country(message):
    code = message.text.upper()
    response = requests.get("https://api.worldbank.org/v2/country/" + code + "?format=json")
    data = response.json()
    info = data[1][0]
    bot.reply_to(message, "🌍 দেশ: " + info["name"] + "\n🏛️ রাজধানী: " + info["capitalCity"] + "\n🌐 অঞ্চল: " + info["region"]["value"])

@bot.message_handler(commands=['age'])
def age(message):
    bot.reply_to(message, "নাম লিখুন:")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    name = message.text
    response = requests.get("https://api.agify.io/?name=" + name)
    data = response.json()
    bot.reply_to(message, "👤 " + name + " নামের গড় বয়স: " + str(data["age"]) + " বছর")

@bot.message_handler(commands=['calc'])
def calc(message):
    bot.reply_to(message, "হিসাব লিখুন (যেমন: 5+3, 10*2):")
    bot.register_next_step_handler(message, get_calc)

def get_calc(message):
    try:
        result = eval(message.text)
        bot.reply_to(message, "🔢 ফলাফল: " + str(result))
    except:
        bot.reply_to(message, "❌ ভুল হিসাব!")

@bot.message_handler(func=lambda message: True)
def reply(message):
    text = message.text.lower()
    if "হ্যালো" in text or "hello" in text:
        bot.reply_to(message, "হ্যালো! কেমন আছেন? 😊")
    elif "কেমন আছো" in text:
        bot.reply_to(message, "আলহামদুলিল্লাহ ভালো আছি! 😄")
    elif "তোমার নাম" in text:
        bot.reply_to(message, "আমার নাম MahadiBot Pro! 🤖")
    elif "ধন্যবাদ" in text:
        bot.reply_to(message, "আপনাকেও ধন্যবাদ! 😊")
    else:
        bot.reply_to(message, "বুঝতে পারিনি! /help দেখুন 😊")

# ===== অটো শিডিউল =====
schedule.every().day.at("07:00").do(send_weather)
schedule.every().day.at("08:00").do(send_news)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=run_schedule).start()
bot.polling()

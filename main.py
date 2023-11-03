import telebot
from telebot import types
import MorseCodeConverter
from decouple import config

TOKEN = config('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    text_to_morse_button = types.KeyboardButton("Text to Morse")
    morse_to_text_button = types.KeyboardButton("Morse to Text")
    markup.add(text_to_morse_button, morse_to_text_button)

    bot.send_message(message.chat.id, "Hello bai, Ako ito ang imong converter!\nPili ka option bai:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Text to Morse")
def text_to_morse(message):
    bot.send_message(message.chat.id, "Type ka ng text na gusto mong iconvert sa morse code bai:")
    bot.register_next_step_handler(message, convert_text_to_morse)

def convert_text_to_morse(message):
    text = message.text
    morse_code = MorseCodeConverter.text_to_morse(text)
    formatted_message = f"<pre><code>{morse_code}</code></pre>"
    
    bot.send_message(message.chat.id, "Morse Code Result", parse_mode="HTML")
    bot.send_message(message.chat.id, formatted_message, parse_mode="HTML")
    start(message)

@bot.message_handler(func=lambda message: message.text == "Morse to Text")
def morse_to_text(message):
    bot.send_message(message.chat.id, "Type ka ng morse code na gusto mong iconvert sa text bai:")
    bot.register_next_step_handler(message, convert_morse_to_text)

def convert_morse_to_text(message):
    morse_code = message.text
    text = MorseCodeConverter.morse_to_text(morse_code)
    formatted_message = f"<pre><code>{text}</code></pre>"
    
    bot.send_message(message.chat.id, "Text Result", parse_mode="HTML")
    bot.send_message(message.chat.id, formatted_message, parse_mode="HTML")
    start(message)

bot.polling()

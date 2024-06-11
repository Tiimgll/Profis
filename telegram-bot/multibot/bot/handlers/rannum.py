from telegram.ext import CommandHandler, CallbackContext
from telegram import Update
from telegram.ext import CallbackContext
import random

def rannum(update: Update, context: CallbackContext) -> None:
    text = context.args
    if not text:
        update.message.reply_text("Пожалуйста, укажите диапазон в формате /rannum min-max")
        return

    try:
        min_value, max_value = map(int, text[0].split('-'))
    except ValueError:
        update.message.reply_text("Недопустимый формат диапазона. Пожалуйста, используйте /rannum min-max")
        return

    def generate_random_number(min_value, max_value):
        return random.randint(min_value, max_value)

    generated_number = generate_random_number(min_value, max_value)

    update.message.reply_text(f"Сгенерированное случайное число ({min_value}-{max_value}): {generated_number}")



handler = CommandHandler("rannum", rannum)
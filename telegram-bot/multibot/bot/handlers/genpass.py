from telegram.ext import CommandHandler, CallbackContext
from telegram import Update
import random
import string

def generate_password(length=12, use_special_chars=False):
    characters = string.ascii_letters + string.digits
    if use_special_chars:
        characters += string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def genpass(update: Update, context: CallbackContext) -> None:
    args = context.args
    if not args or not args[0].isdigit():
        update.message.reply_text("Недопустимый формат. Пожалуйста, используйте /genpass [Длина] [Включать специальные символы]")
        return

    password_length = int(args[0])
    include_special_chars = bool(args[1]) if len(args) > 1 else False

    generated_password = generate_password(password_length)

    update.message.reply_text(f"Сгенерированный пароль: {generated_password}")

handler = CommandHandler("genpass", genpass)

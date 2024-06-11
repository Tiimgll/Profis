from telegram.ext import CommandHandler, CallbackContext
from telegram import Update
from telegram.ext import CallbackContext

def help(update: Update, context: CallbackContext) -> None:
    help_text = (
        "Список доступных команд:\n"
        "/genpass [длина] - генерация пароля\n"
        "/rannum [мин-макс] - генерация случайного числа в заданном диапазоне\n"
        "/timez [europe/america/russia] - вывод текущего времени в часовых поясах\n"
        "/help - получение справки о доступных командах"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

handler = CommandHandler("help", help)

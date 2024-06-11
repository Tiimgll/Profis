from telegram.ext import CommandHandler, CallbackContext
from telegram import Update
from telegram.utils.helpers import mention_html

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    mention = mention_html(user.id, user.first_name)
    update.message.reply_html(
        fr'Привет, {mention}! Я MultiBot. Давай начнем! Чтобы узнать функционал бота используйте команду /help!'
    )

handler = CommandHandler("start", start)

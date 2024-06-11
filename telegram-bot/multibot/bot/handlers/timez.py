from telegram.ext import CommandHandler, CallbackContext
from telegram import Update
from telegram.ext import CallbackContext
from datetime import datetime
import pytz

def timez(update: Update, context: CallbackContext) -> None:
    def get_world_time(timezones):
        time_info = ""
        for continent, timezone in timezones.items():
            try:
                user_timezone = pytz.timezone(timezone)
                current_time = datetime.utcnow()
                user_time = current_time.replace(tzinfo=pytz.utc).astimezone(user_timezone)
                time_info += f"{continent.capitalize()}: {user_time.strftime('%d-%m-%Y %H:%M:%S %Z%z')}\n"
            except pytz.UnknownTimeZoneError:
                time_info += f"{continent.capitalize()}: Неизвестный часовой пояс\n"

        return time_info.strip()

    timezones = {
        'europe': 'Europe/Berlin',
        'america': 'America/New_York',
        'russia': 'Europe/Moscow',
    }

    current_time = get_world_time(timezones)

    update.message.reply_text(current_time)


handler = CommandHandler("timez", timez)
# python 3.9.13
# python-telegram-bot==13.7

from telegram.ext import Updater

from bot import config
from bot.handlers import genpass, rannum, start, timez, help

def main() -> None:
    updater = Updater(config.BOT_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(start.handler)
    dp.add_handler(genpass.handler)
    dp.add_handler(rannum.handler)
    dp.add_handler(timez.handler)
    dp.add_handler(help.handler)




    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
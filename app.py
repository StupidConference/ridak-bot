import nahuy_database
import logging
import re
import os
from random import choice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import sleep

MODIFIER_RANDOM = 40
MODIFIER_TRIGGER = 5
MODIFIER_BOLD = 50


def msg_delay():
    sleep(choice(list(range(1, 7))))


def cmd_help(bot, update):
    update.message.reply_text(text=nahuy_database.help_msg,
                              disable_notification=True,
                              parse_mode='html',
                              quote=True)


def ridak_say_nahuy(bot, update):
    if choice([0, 1]) == 0:
        if choice(list(range(0, MODIFIER_RANDOM))) == 1:
            if choice(list(range(0, MODIFIER_BOLD))) == 1:
                msg_delay()
                update.message.reply_text(text=f'<b>{choice(nahuy_database.random_list)}</b>',
                                          disable_notification=True,
                                          parse_mode='html',
                                          quote=True)
                return
            msg_delay()
            update.message.reply_text(text=choice(nahuy_database.random_list),
                                      disable_notification=True,
                                      quote=True)
    else:
        for i in update.message.text.split():
            for n in nahuy_database.trigger_words:
                if re.match(n, i):
                    if choice(list(range(0, MODIFIER_TRIGGER))) == 1:
                        msg_delay()
                        update.message.reply_text(text=choice(nahuy_database.trigger_result),
                                                  disable_notification=True,
                                                  quote=True)


if __name__ == "__main__":
    TOKEN = os.environ['TOKEN']
    PORT = os.environ.get('PORT')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, ridak_say_nahuy))
    dp.add_handler(CommandHandler('start', cmd_help))
    dp.add_handler(CommandHandler('help', cmd_help))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(f'https://ridak-bot.herokuapp.com/{TOKEN}')
    updater.idle()

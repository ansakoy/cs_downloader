import os

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton

from csdbot_token import TOKEN
from launch import launch


# SCRIPT GLOBALS
NORMAL_MODE = False
PARAMS_UPLOADED = False

# FIELDS
TASK = 'task'
EXT = 'ext'
SPAN = 'span'
MODE = 'mode'

# Значения клавиатуры
DEMO = 'Режим ДЕМО'
NORMAL = 'Нормальный режим'
INFO = 'ИНФО'
CONTR = 'По контрактам'
PROD = 'По продуктам'
CSV = 'CSV'
XLSX = 'XLSX'
JSON = 'JSON'


keyboard_mode = [[KeyboardButton(text=DEMO),
             KeyboardButton(text=NORMAL)]]
markup_mode = ReplyKeyboardMarkup(keyboard_mode, one_time_keyboard=True)

keyboard_task = [[KeyboardButton(text=INFO),
             KeyboardButton(text=CONTR),
             KeyboardButton(text=PROD)]]
markup_task = ReplyKeyboardMarkup(keyboard_task, one_time_keyboard=True)

keyboard_ext = [[KeyboardButton(text=CSV),
             KeyboardButton(text=XLSX),
             KeyboardButton(text=JSON)]]
markup_ext = ReplyKeyboardMarkup(keyboard_ext, one_time_keyboard=True)


def is_normal_mode(choice):
    return choice == NORMAL


def doc_handler(bot, update):
    print('worked')
    received_file = bot.getFile(update.message.document.file_id)
    print("file_id: " + str(update.message.document.file_id))
    received_file.download('params/params_csv.csv')
    PARAMS_UPLOADED = True


def start(bot, update):
    update.message.reply_text("Выберите режим", reply_markup=markup_mode)


def upload(bot, update, user_data):
    mode = update.message.text
    print(mode)
    # mode = RegexHandler('^(Режим ДЕМО|Нормальный режим)$', start, pass_user_data=True)
    # if is_normal_mode(mode):
    #     NORMAL_MODE = True
    #     update.message.reply_text("Пришлите файл CSV с параметрами")

#
# def task()
#
#
# def sos(bot, update):
#     pass

#
# updater = Updater(token=TOKEN)
# dispatcher = updater.dispatcher
# start_handler = CommandHandler('start', start)
# help_handler = CommandHandler('help', sos)
# conversation_handler = ConversationHandler(
#             entry_points=[start_handler],
#             states={MODE: [RegexHandler('^(Режим ДЕМО|Нормальный режим)$', upload, pass_user_data=True)],
#                     GROUP: [RegexHandler('^(Режим ДЕМО|Нормальный режим)$', group, pass_user_data=True)],
#                     BY_VAL: [RegexHandler('^(Yes|No)$', by_val, pass_user_data=True)]},
#             fallbacks=[CommandHandler('start', start)],
#             allow_reentry=True)
# dispatcher.add_handler(MessageHandler(Filters.document, doc_handler))
# dispatcher.add_handler(help_handler)



if __name__ == '__main__':
    # Регистрация команд и запуск бота
    # updater = Updater(token=TOKEN)
    # dispatcher = updater.dispatcher
    # fromfile_handler = CommandHandler('fromf', fromfile)
    # dispatcher.add_handler(fromfile_handler)
    # updater.start_polling()
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    conversation_handler = ConversationHandler(
                entry_points=[start_handler],
                states={MODE: [RegexHandler('^(Режим ДЕМО|Нормальный режим)$', upload, pass_user_data=True)]},
                fallbacks=[start_handler],
                allow_reentry=True)
    dispatcher.add_handler(MessageHandler(Filters.document, doc_handler))
    # dispatcher.add_handler(start_handler)
    dispatcher.add_handler(conversation_handler)
    updater.start_polling()

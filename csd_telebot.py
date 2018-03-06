import os

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton

from csdbot_token import TOKEN
from launch import launch


# SCRIPT GLOBALS
NORMAL_MODE = False
PARAMS_UPLOADED = False
LAUNCH_TEXT = 'ПАРАМЕТРЫ ОПЕРАЦИИ:\n'
FNAME = None

# FIELDS
TASK = 'task'
EXT = 'ext'
SPAN = 'span'
MODE = 'mode'
UPLOAD = 'upload'
LAUNCH = 'launch'

# Значения клавиатуры
DEMO = 'Демо'
NORMAL = 'Обычный'
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

keyboard_launch = [[KeyboardButton(text='Запуск')]]
markup_launch = ReplyKeyboardMarkup(keyboard_ext, one_time_keyboard=True)


DIALOG_MAPPING = {MODE: 0,
                UPLOAD: 1,
                TASK: 2,
                EXT: 3,
                SPAN: 4,
                LAUNCH: 5}


def is_demo(choice):
    return choice == DEMO


def get_task_code(choice):
    if choice == PROD:
        return 'BY_PRODUCT'
    elif choice == CONTR:
        return 'BY_CONTRACT'
    else:
        return 'INFO'


def process_span(number):
    try:
        return int(number)
    except:
        return 'Вы ввели некорректный параметр. Число дней указывается целым числом. Попробуйте еще раз или нажмите "Запуск".'


# def doc_handler(bot, update):
#     print('worked')
#     received_file = bot.getFile(update.message.document.file_id)
#     print("file_id: " + str(update.message.document.file_id))
#     received_file.download('params/params_csv.csv')
#     PARAMS_UPLOADED = True


def start(bot, update):
    update.message.reply_text("Выберите режим", reply_markup=markup_mode)
    return 0


def mode(bot, update, user_data):
    mode = update.message.text
    LAUNCH_TEXT += 'Режим: {}\n'.format(mode)
    print(mode, is_normal_mode(mode))
    user_data['demo'] = is_demo(mode)
    if is_demo(mode):
        update.message.reply_text("Выберите задачу", reply_markup=markup_task)
        return 2
    print('Normal mode is', NORMAL_MODE)
    NORMAL_MODE = True
    return 1


def upload(bot, update, user_data):
    if not (NORMAL_MODE and PARAMS_UPLOADED):
        update.message.reply_text("Пришлите файл CSV с параметрами")
        received_file = bot.getFile(update.message.document.file_id)
        if received_file:
            PARAMS_UPLOADED = True
        received_file.download('params/params_csv.csv')
        return 1
    update.message.reply_text("Выберите задачу", reply_markup=markup_task)
    return 2


def task(bot, update, user_data):
    task = update.message.text
    user_data['task'] = get_task_code(task)
    print(task)
    if task == PROD or task == CONTR:
        FNAME = '{}'.format(update.message.chat_id)
        LAUNCH_TEXT += 'Задача: выгрузка "{}"\n'.format(task)
        update.message.reply_text("Выберите формат файла", reply_markup=markup_ext)
        return 3
    else:
        LAUNCH_TEXT += 'Задача: Вывести информацию о запросе\n'
        update.message.reply_text("Вы можете указать число дней в подпериодах, на которые может быть разбит период для дробления запроса. Число дней указывается целым числом. Если вы не хотите указывать этот параметр, просто нажмите кнопку 'Запуск'", reply_markup=markup_launch)
        return 4


def outformat(bot, update, user_data):
    outf = update.message.text
    user_data['format'] = outf
    print(outf)
    LAUNCH_TEXT += 'Формат выгрузки: {}\n'.format(outf)
    update.message.reply_text("Вы можете указать число дней в подпериодах, на которые может быть разбит период для дробления запроса. Число дней указывается целым числом. Если вы не хотите указывать этот параметр, просто нажмите кнопку 'Запуск'", reply_markup=markup_launch)
    return 4


def add_span(bot, update, user_data):
    choice = update.message.text
    if choice == 'Запуск':
        return 5
    span = process_span(choice)
    if type(span) is str:
        update.message.reply_text(span)
        return 4
    user_data['span'] = span
    LAUNCH_TEXT += 'Длина подпериодов (в днях): {}\n'.format(span)
    return 5


def launch_launch(bot, update, user_data):
    LAUNCH_TEXT += 'Приступаю к выполнению. В зависимости от размера выгрузки операция может занять некоторое время.'
    result = launch.launch(source='params/params_csv.csv',
                    task=user_data['task'],
                    out_format=user_data.get('format', 'CSV'),
                    span=user_data.get('span', 30),
                    out_name=FNAME
                    demo=user_data['demo'])
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=result)
    user_data.clear()
    return ConversationHandler.END


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
                states={0: [RegexHandler('^(Режим ДЕМО|Нормальный режим)$', mode, pass_user_data=True)]},
                        {1: [MessageHandler(Filters.document, upload, pass_user_data=True)]},
                        {2: [RegexHandler('^(ИНФО|По контрактам|По продуктам)$', task, pass_user_data=True)]},
                        {3: [RegexHandler('^(CSV|XLSX|JSON)$', task, pass_user_data=True)]},
                        {4: [RegexHandler('^(CSV|XLSX|JSON)$', task, pass_user_data=True)]},
                fallbacks=[start_handler],
                allow_reentry=True)
    # dispatcher.add_handler(MessageHandler(Filters.document, doc_handler))
    # dispatcher.add_handler(start_handler)
    dispatcher.add_handler(conversation_handler)
    updater.start_polling()

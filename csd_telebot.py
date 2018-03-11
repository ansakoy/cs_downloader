import os
import json

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton

import logging

from csdbot_token import TOKEN
import launch
import downloader.api_builder as api_builder
import downloader.settings as settings
import downloader.process as process
import downloader.daterange_processor as daterange_processor

# USER_DATA FIELDS
MODE_CHOICE = 'mode_choice'
TASK = 'task'
EXT = 'ext'
SPAN = 'span'
DEMO = 'demo'
UPLOAD = 'upload'
LAUNCH = 'launch'
LAUNCH_TEXT = 'launch_text'
PARAMS_TEXT = 'params_text'
FNAME = 'fname'
OUTF = 'outf'
EXTENSION = 'extension'
PARAMS_SOURCE = 'params_source'
EMAIL = 'email'

# Значения клавиатуры
DEMO_MODE = 'Демо'
NORMAL = 'Обычный'
INFO = 'ИНФО'
CONTR = 'По контрактам'
PROD = 'По продуктам'
CSV = 'CSV'
XLSX = 'XLSX'
JSON = 'JSON'
START = 'Запуск'
CANCEL = 'Снять задачу'


DATERANGE = 'daterange'


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


keyboard_mode = [[KeyboardButton(text=DEMO_MODE),
             KeyboardButton(text=NORMAL),
             KeyboardButton(text=CANCEL)]]
markup_mode = ReplyKeyboardMarkup(keyboard_mode, one_time_keyboard=True)

keyboard_task = [[KeyboardButton(text=INFO),
             KeyboardButton(text=CONTR),
             KeyboardButton(text=PROD),
             KeyboardButton(text=CANCEL)]]
markup_task = ReplyKeyboardMarkup(keyboard_task, one_time_keyboard=True)

keyboard_ext = [[KeyboardButton(text=CSV),
             KeyboardButton(text=XLSX),
             KeyboardButton(text=JSON),
             KeyboardButton(text=CANCEL)]]
markup_ext = ReplyKeyboardMarkup(keyboard_ext, one_time_keyboard=True)

keyboard_cancel = keyboard_launch = [[KeyboardButton(text=CANCEL)]]
markup_cancel = ReplyKeyboardMarkup(keyboard_cancel, one_time_keyboard=True)

keyboard_launch = [[KeyboardButton(text=START),
                KeyboardButton(text=CANCEL)]]
markup_launch = ReplyKeyboardMarkup(keyboard_launch, one_time_keyboard=True)


DIALOGUE = {MODE_CHOICE: 0,
                UPLOAD: 1,
                TASK: 2,
                EXT: 3,
                EMAIL: 4,
                SPAN: 5}


def dump_json(dictionary, json_file):

    # Записать словарь в виде файла json

    with open(json_file, 'w', encoding='utf-8') as handler:
        json.dump(dictionary, handler, ensure_ascii=False)


def is_demo(choice):
    return choice == DEMO_MODE


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


def get_fextension(choice):
    if choice == XLSX:
        return '.xlsx'
    elif choice == JSON:
        return '.json'
    return '.csv'


def process_params(file_location=None, demo=False):
    if demo:
        params = settings.DEFAULT_PARAMS
    else:
        params = process.get_params_from_csv(file_location)
    if not api_builder.has_valid_fields(params):
        return settings.WRONG_PARAMS_MSG
    if not params.get(DATERANGE):
        default = daterange_processor.get_default_daterange()
        daterange = daterange_processor.date_to_str(default)
        query_info = launch.get_query_info_text(params, daterange)
        return query_info
    query_info = launch.get_query_info_text(params)
    return query_info


def get_filename(chat_id):
    data_files = os.listdir('data')
    max_val = -1
    for entry in data_files:
        if entry.startswith(str(chat_id)):
            num = int(entry.split('.')[0].split('_')[1])
            if num > max_val:
                max_val = num
    return str(chat_id) + '_' + str(max_val + 1)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def start(bot, update):
    update.message.reply_text("Выберите режим", reply_markup=markup_mode)
    return DIALOGUE[MODE_CHOICE]

import test_bot
from threading import Thread


def test(bot, update):
    update.message.reply_text("type sleep in seconds")
    return 0


def test_test(bot, update, user_data):
    chat_id = update.message.chat_id
    print(chat_id)
    sec = update.message.text
    print(sec)

def thread_launch(sec):
    os.system('python test_bot.py {}'.format(sec))


def mode(bot, update, user_data):
    mode = update.message.text
    if mode == CANCEL:
        update.message.reply_text('Задача снята.')
        if user_data.get(PARAMS_SOURCE):
            os.remove(user_data[PARAMS_SOURCE])
        user_data.clear()
        return ConversationHandler.END
    user_data[DEMO] = is_demo(mode)
    user_data[LAUNCH_TEXT] = 'Параметры операции:\n'
    user_data[LAUNCH_TEXT] += 'Режим: {}\n'.format(mode)
    if is_demo(mode):
        update.message.reply_text("Выберите задачу", reply_markup=markup_task)
        user_data[PARAMS_TEXT] = process_params(demo=True)
        return DIALOGUE[TASK]
    update.message.reply_text("Пришлите файл CSV с параметрами", reply_markup=markup_cancel)
    return DIALOGUE[UPLOAD]


def upload(bot, update, user_data):
    chat_id = update.message.chat_id
    cancel = update.message.text
    print(cancel)
    if cancel:
        update.message.reply_text('Задача снята.')
        if user_data.get(PARAMS_SOURCE):
            os.remove(user_data[PARAMS_SOURCE])
        user_data.clear()
        return ConversationHandler.END
    received_file = bot.getFile(update.message.document.file_id)
    # print(received_file)
    if received_file['file_path'].endswith('.csv'):
        params_name = 'params_{}.csv'.format(chat_id)
        received_file.download(os.path.join('params', params_name))
        user_data[PARAMS_SOURCE] = os.path.join('params', params_name)
        check = process_params(file_location=user_data[PARAMS_SOURCE])
        if check == settings.WRONG_PARAMS_MSG:
            update.message.reply_text(check + 'Попробуйте исправить заполнение параметров и пришлите файл снова.')
            return DIALOGUE[UPLOAD]
        update.message.reply_text("Выберите задачу", reply_markup=markup_task)
        user_data[PARAMS_SOURCE] = os.path.join('params', params_name)
        user_data[PARAMS_TEXT] = check
        return DIALOGUE[TASK]
    update.message.reply_text("Неверный формат файла. Пришлите файл CSV с параметрами.")
    return DIALOGUE[UPLOAD]


def task(bot, update, user_data):
    task = update.message.text
    user_data[TASK] = get_task_code(task)
    if task == PROD or task == CONTR:
        user_data[FNAME] = get_filename(update.message.chat_id)
        user_data[LAUNCH_TEXT] += 'Задача: выгрузка "{}"\n'.format(task)
        update.message.reply_text("Выберите формат файла", reply_markup=markup_ext)
        return DIALOGUE[EXT]
    elif task == CANCEL:
        update.message.reply_text('Задача снята.')
        if user_data.get(PARAMS_SOURCE):
            os.remove(user_data[PARAMS_SOURCE])
        user_data.clear()
        return ConversationHandler.END
    user_data[LAUNCH_TEXT] += 'Задача: Вывести информацию о запросе\n'
    update.message.reply_text('Укажите адрес электронной почты, куда будет отправлен выгруженный файл', reply_markup=markup_cancel)
    return DIALOGUE[EMAIL]


def outformat(bot, update, user_data):
    outf = update.message.text
    if outf == CANCEL:
        update.message.reply_text('Задача снята.')
        if user_data.get(PARAMS_SOURCE):
            os.remove(user_data[PARAMS_SOURCE])
        user_data.clear()
        return ConversationHandler.END
    user_data[OUTF] = outf
    user_data[LAUNCH_TEXT] += 'Формат выгрузки: {}\n'.format(outf)
    user_data[EXTENSION] = get_fextension(outf)
    update.message.reply_text('Укажите адрес электронной почты, куда будет отправлен выгруженный файл', reply_markup=markup_cancel)
    return DIALOGUE[EMAIL]


def email(bot, update, user_data):
    email = update.message.text
    if '@' not in email or '.' not in email.split('@')[-1]:
        update.message.reply_text("Вы указали некорректный email", reply_markup=markup_cancel)
        return DIALOGUE[EMAIL]
    elif email == CANCEL:
        update.message.reply_text('Задача снята.')
        if user_data.get(PARAMS_SOURCE):
            os.remove(user_data[PARAMS_SOURCE])
        user_data.clear()
        return ConversationHandler.END
    user_data[EMAIL] = email
    # print(user_data[EMAIL])
    update.message.reply_text("Вы можете указать число дней в подпериодах, на которые может быть разбит период для дробления запроса. Число дней указывается целым числом. Если вы не хотите указывать этот параметр, просто нажмите кнопку 'Запуск'", reply_markup=markup_launch)
    return DIALOGUE[SPAN]


def add_span(bot, update, user_data):
    choice = update.message.text
    print(choice)
    if choice == START:
        redirect_to_launch(bot, update, user_data)
        return ConversationHandler.END
    elif choice == CANCEL:
        update.message.reply_text('Задача снята.')
        if user_data.get(PARAMS_SOURCE):
            os.remove(user_data[PARAMS_SOURCE])
        user_data.clear()
        return ConversationHandler.END
    span = process_span(choice)
    if type(span) is str:
        update.message.reply_text(span)
        return DIALOGUE[SPAN]
    user_data['span'] = span
    user_data[LAUNCH_TEXT] += 'Длина подпериодов (в днях): {}\n'.format(span)
    update.message.reply_text("Теперь можно запустить скрипт или отказаться от запуска", reply_markup=markup_launch)
    return DIALOGUE[SPAN]


# def launch_launch(bot, update, user_data):
#     chat_id = update.message.chat_id
#     # bot.send_message(chat_id=chat_id, text=user_data[PARAMS_TEXT])
#     user_data[LAUNCH_TEXT] += '\n' + user_data[PARAMS_TEXT]
#     user_data[LAUNCH_TEXT] += '\n\nПриступаю к выполнению. В зависимости от объема задачи операция может занять от нескольких секунд до нескольких часов.'
#     bot.send_message(chat_id=chat_id, text=user_data[LAUNCH_TEXT])
#     result = launch.launch(source=user_data.get(PARAMS_SOURCE),
#                     task=user_data[TASK],
#                     out_format=user_data.get(OUTF, 'CSV'),
#                     span=user_data.get(SPAN, 30),
#                     out_name=user_data.get(FNAME),
#                     demo=user_data[DEMO])
#     if user_data.get(FNAME):
#         f_path = os.path.join('data', user_data[FNAME] + user_data[EXTENSION])
#         bot.send_document(chat_id=chat_id, document=open(f_path, 'rb'))
#         os.remove(f_path)
#     if user_data.get(PARAMS_SOURCE):
#         os.remove(user_data[PARAMS_SOURCE])
#     bot.send_message(chat_id=chat_id, text=result)
#     user_data.clear()


def redirect_to_launch(bot, update, user_data):
    chat_id = update.message.chat_id
    msg = 'Скрипт запущен. В зависимости от объема задачи  и количества запросов от разных пользователей операция может занять от нескольких секунд до нескольких часов. Результат будет отправлен по адресу {}.'.format(user_data[EMAIL])
    bot.send_message(chat_id=chat_id, text=msg)
    usrdata_path = os.path.join('usrdata', 'usrdata{}.json'.format(chat_id))
    dump_json(user_data, usrdata_path)
    user_data.clear()


def sos(bot, update):
    chat_id = update.message.chat_id
    text = '''
        Этот бот позволяет выгружать информацию о контрактах, заключенных по 94-ФЗ, 44-ФЗ и 223-ФЗ, через API проекта "Госзатраты" (clearspendng.ru).
        Также он позволяет получать следующую информацию о запросе:
        - Есть ли в принципе отвечающие запросы контракты;
        - Если есть, то сколько их;
        - Предупреждение, если запрос не позволяет выдать выгрузить все контракты из-за технических ограничений.
        Возможные форматы выгрузки:
        - CSV;
        - XLSX;
        - JSON.
        В формате JSON выгружаются все имеющиеся данные о контрактах.
        В остальных форматах выгружаются только некоторые поля. В зависимости от потребностей пользователя выгрузка может производиться в двух режимах:
        - одна строка таблицы - один контракт;
        - одна строка таблицы - один продукт.
        Подробнее с документацией можно ознакомиться здесь:
        https://github.com/ansakoy/cs_downloader/wiki
        Чтобы запустить бот, наберите /start.
        Чтобы протестировать его работу с параметрами запроса по умолчанию, используйте режим "Демо".
        Чтобы задать свои параметры запроса, необходимо использовать файл CSV (см. инструкцию: https://github.com/ansakoy/cs_downloader/wiki/Параметры-запроса)
    '''
    bot.send_message(chat_id=chat_id, text=text)


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', sos)
    test_handler = CommandHandler('test', test)
    test_dialogue_handler = ConversationHandler(
                entry_points=[test_handler],
                states={0: [RegexHandler('^([0-9]+)$', test_test, pass_user_data=True)]
                },
                fallbacks=[test_handler],
                allow_reentry=True)

    conversation_handler = ConversationHandler(
                entry_points=[start_handler],
                states={0: [RegexHandler('^(Демо|Обычный|Снять задачу)$', mode, pass_user_data=True)],
                        1: [MessageHandler(Filters.document, upload, pass_user_data=True), RegexHandler('^(Снять задачу)$', upload, pass_user_data=True)],
                        2: [RegexHandler('^(ИНФО|По контрактам|По продуктам|Снять задачу)$', task, pass_user_data=True)],
                        3: [RegexHandler('^(CSV|XLSX|JSON|Снять задачу)$', outformat, pass_user_data=True)],
                        4: [RegexHandler('^(.+@.+\..+|Снять задачу|Снять задачу)$', email, pass_user_data=True)],
                        5: [RegexHandler('^(Запуск|Снять задачу|[0-9]+)$', add_span, pass_user_data=True)]},
                fallbacks=[start_handler],
                allow_reentry=True)
    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(test_dialogue_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()

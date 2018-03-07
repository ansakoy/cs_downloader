import os

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton

from csdbot_token import TOKEN
import launch

# USER_DATA FIELDS
MODE_CHOICE = 'mode_choice'
TASK = 'task'
EXT = 'ext'
SPAN = 'span'
DEMO = 'demo'
UPLOAD = 'upload'
LAUNCH = 'launch'
PARAMS_UPLOADED = 'params_uploaded'
LAUNCH_TEXT = 'launch_text'
FNAME = 'fname'
OUTF = 'outf'
EXTENSION = 'extension'
PARAMS_SOURCE = 'params_source'

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


keyboard_mode = [[KeyboardButton(text=DEMO_MODE),
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

keyboard_launch = [[KeyboardButton(text=START),
                KeyboardButton(text=CANCEL)]]
markup_launch = ReplyKeyboardMarkup(keyboard_launch, one_time_keyboard=True)


DIALOGUE = {MODE_CHOICE: 0,
                UPLOAD: 1,
                TASK: 2,
                EXT: 3,
                SPAN: 4}


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


# def doc_handler(bot, update):
#     print('worked')
#     received_file = bot.getFile(update.message.document.file_id)
#     print("file_id: " + str(update.message.document.file_id))
#     received_file.download('params/params_csv.csv')
#     PARAMS_UPLOADED = True


def start(bot, update):
    update.message.reply_text("Выберите режим", reply_markup=markup_mode)
    return DIALOGUE[MODE_CHOICE]


def mode(bot, update, user_data):
    mode = update.message.text
    user_data[DEMO] = is_demo(mode)
    user_data[LAUNCH_TEXT] = 'ПАРАМЕТРЫ ОПЕРАЦИИ:\n'
    user_data[LAUNCH_TEXT] += 'Режим: {}\n'.format(mode)
    print(user_data[LAUNCH_TEXT])
    if is_demo(mode):
        update.message.reply_text("Выберите задачу", reply_markup=markup_task)
        print(DIALOGUE[TASK])
        return DIALOGUE[TASK]
    return DIALOGUE[UPLOAD]


def upload(bot, update, user_data):
    if not (NORMAL_MODE and PARAMS_UPLOADED):
        update.message.reply_text("Пришлите файл CSV с параметрами")
        received_file = bot.getFile(update.message.document.file_id)
        if received_file:
            PARAMS_UPLOADED = True
        received_file.download(os.path.join('params', 'params_telebot.csv'))
        return DIALOGUE[UPLOAD]
    update.message.reply_text("Выберите задачу", reply_markup=markup_task)
    user_data[PARAMS_SOURCE] = os.path.join('params', 'params_telebot.csv')
    return DIALOGUE[TASK]


def task(bot, update, user_data):
    task = update.message.text
    user_data[TASK] = get_task_code(task)
    print(task)
    if task == PROD or task == CONTR:
        user_data[FNAME] = '{}'.format(update.message.chat_id)
        user_data[LAUNCH_TEXT] += 'Задача: выгрузка "{}"\n'.format(task)
        print(user_data[LAUNCH_TEXT])
        update.message.reply_text("Выберите формат файла", reply_markup=markup_ext)
        return DIALOGUE[EXT]
    user_data[LAUNCH_TEXT] += 'Задача: Вывести информацию о запросе\n'
    print(user_data[LAUNCH_TEXT])
    update.message.reply_text('Вы можете указать число дней в подпериодах, на которые может быть разбит период для дробления запроса. Число дней указывается целым числом. Если вы не хотите указывать этот параметр, просто нажмите кнопку "Запуск"', reply_markup=markup_launch)
    return DIALOGUE[SPAN]


def outformat(bot, update, user_data):
    outf = update.message.text
    user_data[OUTF] = outf
    print(outf)
    user_data[LAUNCH_TEXT] += 'Формат выгрузки: {}\n'.format(outf)
    user_data[EXTENSION] = get_fextension(outf)
    update.message.reply_text("Вы можете указать число дней в подпериодах, на которые может быть разбит период для дробления запроса. Число дней указывается целым числом. Если вы не хотите указывать этот параметр, просто нажмите кнопку 'Запуск'", reply_markup=markup_launch)
    return DIALOGUE[SPAN]


def add_span(bot, update, user_data):
    choice = update.message.text
    if choice == START:
        launch_launch(bot, update, user_data)
        return ConversationHandler.END
    elif choice == CANCEL:
        update.message.reply_text('Задача снята.')
        if not user_data[DEMO]:
            os.remove(os.path.join('params', 'params_telebot.csv'))
        return ConversationHandler.END
    span = process_span(choice)
    if type(span) is str:
        update.message.reply_text(span)
        return DIALOGUE[SPAN]
    user_data['span'] = span
    user_data[LAUNCH_TEXT] += 'Длина подпериодов (в днях): {}\n'.format(span)
    launch_launch(bot, update, user_data)


def launch_launch(bot, update, user_data):
    chat_id = update.message.chat_id
    user_data[LAUNCH_TEXT] += 'Приступаю к выполнению. В зависимости от объема задачи операция может занять от нескольких секунд до нескольких часов.'
    bot.send_message(chat_id=chat_id, text=user_data[LAUNCH_TEXT])
    if user_data.get(FNAME):
        print(user_data[FNAME])
    result = launch.launch(source=user_data.get(PARAMS_SOURCE),
                    task=user_data[TASK],
                    out_format=user_data.get(OUTF, 'CSV'),
                    span=user_data.get(SPAN, 30),
                    out_name=user_data.get(FNAME),
                    demo=user_data[DEMO])
    print('hello world')
    if user_data.get(FNAME):
        f_path = os.path.join('data', user_data[FNAME] + user_data[EXTENSION])
        print(f_path)
        bot.send_document(chat_id=chat_id, document=open(f_path, 'r'))
        os.remove(f_path)
    bot.send_message(chat_id=chat_id, text=result)
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
        ССЫЛКА!
    '''
    bot.send_message(chat_id=chat_id, text=text)


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', sos)
    conversation_handler = ConversationHandler(
                entry_points=[start_handler],
                states={0: [RegexHandler('^(Демо|Обычный)$', mode, pass_user_data=True)],
                        1: [MessageHandler(Filters.document, upload, pass_user_data=True)],
                        2: [RegexHandler('^(ИНФО|По контрактам|По продуктам)$', task, pass_user_data=True)],
                        3: [RegexHandler('^(CSV|XLSX|JSON)$', outformat, pass_user_data=True)],
                        4: [RegexHandler('^(Запуск|Снять задачу|.)$', add_span, pass_user_data=True)]},
                fallbacks=[start_handler],
                allow_reentry=True)
    # dispatcher.add_handler(MessageHandler(Filters.document, doc_handler))
    # dispatcher.add_handler(start_handler)
    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(help_handler)
    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()

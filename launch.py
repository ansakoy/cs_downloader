'''
Модуль проверяет корректность запроса и определяет сценарий выполнения
задачи.
'''
import os
import time

import downloader.process as process
import downloader.api_builder as api_builder
import downloader.daterange_processor as daterange_processor
from downloader.settings import *


def get_query_info_text(params, daterange=None):
    text = 'Параметры запроса:'
    for key in params:
        text += '\n' + key + ': ' + params[key]
    if daterange:
        text += '\ndaterange по умолчанию: ' + daterange
    return text


def convert_running_time(value):
    minutes, seconds = divmod(value, 60)
    hours, minutes = divmod(minutes, 60)
    return 'Время работы скрипта: %d:%02d:%02d' % (hours, minutes, seconds)


# def send_to_telebot(bot, chat_id):
#     updater = Updater(token=TOKEN)
#     dispatcher = updater.dispatcher/.


def launch(source=None, task='INFO', out_format='CSV', out_name=None, span=30,
            demo=False):
    start = time.time()
    if demo:
        # При demo=True используются параметры запроса по умолчанию [из settings].
        params = DEFAULT_PARAMS
    elif not source:
        # Если источник не указан, ищется файл params.csv с параметрами в папке cs_downloader.params
        default_location = os.path.join(PARAMS_DIR, PARAMS_FILE)
        params = process.get_params_from_csv(default_location)

    elif source and source.endswith('.csv'):
        params = process.get_params_from_csv(source)
    elif source and source.endswith('.txt'):
        params = process.get_params_from_txt(source)
    else:
        print(NO_PARAMS_MSG)
        return NO_PARAMS_MSG

    # Если с параметрами что-то не в порядке
    if type(params) is str:
        print(params)
        return params
    if not api_builder.has_valid_fields(params):
        print(WRONG_PARAMS_MSG)
        return WRONG_PARAMS_MSG

    strategy = api_builder.choose_strategy(params)
    query_date = api_builder.build_query(strategy, params)
    api_base = query_date[0]
    daterange_str = query_date[1]
    date_for_output = None
    if not daterange_str:
        begin, end = daterange_processor.get_default_daterange()
        daterange_str = daterange_processor.date_to_str(begin, end)
        date_for_output = daterange_str
    query_info = get_query_info_text(params, date_for_output)
    print(query_info)

    if task == 'INFO':
        result = process.get_query_info(api_base, daterange_str, strategy, span)
        print(result)
        stop = time.time()
        print(convert_running_time(stop - start))
        return result + '\n' + convert_running_time(stop - start)

    elif task == 'BY_CONTRACT' or task == 'BY_PRODUCT':
        result = process.extract_data(api_base, daterange_str, strategy, out_format, out_name, span, task)
        print(result)
        stop = time.time()
        print(convert_running_time(stop - start))
        return result + '\n' + convert_running_time(stop - start)

    else:
        print('Указана некорректная задача.')
        return 'Указана некорректная задача.'


if __name__ == '__main__':
    launch(source='downloader/contr_params.csv', task='BY_PRODUCT', out_format='JSON', out_name='small_msk')
    # launch(task='CSV')

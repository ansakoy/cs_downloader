'''
Содержит ключевые переменные, используемые в процессе работы
'''

import downloader.daterange_processor as drp


# ПЕРЕМЕННЫЕ
PARAMS = 'params'  # параметры запроса
TASK = 'task'  # Задача (вывод информации/по контрактам/по продуктам)
OUT_FORMAT = 'out_format'  # Формат файла выгрузки
OUT_NAME = 'out_name'  # Название файла выгрузки
SPAN = 'span'  # Длина периодов, на которые будет разбит общий период
STRATEGY = 'strategy'  # Заросы SEARCH или SELECT
DEMO = 'demo'  # Демо-режим (все параметры по умолчанию)



# ПРЕДУПРЕЖДЕНИЯ
WRONG_PARAMS_MSG = 'Запрос содержит некорректные параметры и не может быть обработан.'
NO_PARAMS_MSG = 'Вы не задали параметры. Запрос не может быть обработан. Для демонстрационной выгрузки используйте режим DEMO'


# ИНФОРМАЦИЯ О ЗАДАЧЕ
TASK_INFO = dict()  # Заполняется на основании пользовательского запроса в launch.launch

DEFAULT_PARAMS = {'customerregion': '77',
                  'daterange': drp.date_to_str(drp.get_default_daterange()[0],
                                               drp.get_default_daterange()[1]),
                  'fz': '44'}

PARAMS_DIR = 'params'
PARAMS_FILE = 'params.csv'

# Результат
OUTPUT_PATH = ''
DONE_MSG = 'Готово. Путь к сохраненному файлу: {}'.format(OUTPUT_PATH)

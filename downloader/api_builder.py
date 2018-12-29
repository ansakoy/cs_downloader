# -*- coding: utf-8 -*-

'''
Модуль загружает заданные параметры из файла;
Проверяет их на корректность;
Определяет стратегию выгрузки;
Формирует запрос к API с требуемыми параметрами.
'''

import csv
import json
import os


SELECT = 'http://openapi.clearspending.ru/restapi/v3/contracts/select/?'
SEARCH = 'http://openapi.clearspending.ru/restapi/v3/contracts/search/?'

VALID_FIELDS = ['productsearch', 'okdp_okpd',
                'productsearchlist', 'regnum', 'customerinn',
                'customerkpp', 'supplierinn', 'supplierkpp',
                'customerregion', 'currentstage', 'daterange',
                'pricerange', 'fz']
SEARCH_FIELDS = ['productsearch', 'okdp_okpd',
                'productsearchlist']
DATERANGE = 'daterange'

def has_valid_fields(params_dict):
    '''
    Проверить валидность полей
    '''
    for key in params_dict:
        if key not in VALID_FIELDS:
            return False
    return True


def choose_strategy(params_dict):
    '''
    Выбрать тип запроса к API (SELECT или SEARCH)
    '''
    for entry in SEARCH_FIELDS:
        if entry in params_dict:
            return SEARCH
    return SELECT


def build_query(strategy, params):
    '''
    Сформировать URL-запроса, исключая временной диапазон.
    Диапазон возвращается для дальнейшей обработки вторым элементом tuple
    Первый элемент tuple - сформированный URL-запрос
    '''
    url = strategy
    daterange_value = None
    for param in params:
        if param != DATERANGE:
            url += '&{}={}'.format(param, params[param])
        else:
            daterange_value = params[param]
    return url, daterange_value


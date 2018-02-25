# -*- coding: utf-8 -*-

'''
Модуль обрабатывает информацию по временному диапазону запроса.
Этот параметр используется в качестве дробящего фильтра при запросах SEARCH.
Если временной диапазон в запросе не указан, формируется диапазон
по умолчанию.
'''

import os
import datetime

YEAR = 365
MONTH = 30
WEEK = 7

def str_to_date(date_range):
    '''
    Конвертировать даты начала и конца периода из str в datetime
    '''
    period = date_range.split('-')
    begin = datetime.datetime.strptime(period[0], '%d.%m.%Y')
    end = datetime.datetime.strptime(period[1], '%d.%m.%Y')
    return begin, end


def get_default_daterange(period=MONTH):
    '''
    Рассчитать даты начала и конца периода по умолчанию.
    В качестве конечной даты возвращает дату запроса.
    В качестве начальной - дату за указанное число дней до даты запрос.
    '''
    end = datetime.datetime.now()
    begin = end - datetime.timedelta(period)
    return begin, end


def date_to_str(begin, end):
    '''
    Конвертировать начальную и конечную даты диапазона в строку в формате,
    который требуется документацией API Госзатрат.
    '''
    return begin.strftime('%d.%m.%Y') + '-' + end.strftime('%d.%m.%Y')


def split_daterange(begin, end, span):
    '''
    Разбить заданный период на отрезки длиной в span дней.
    Возвращает список таких отрезков, отформатированных для API-запроса.
    '''
    diff = end - begin
    if diff.days <= span:
        return [date_to_str(begin, end)]
    date_ranges = list()
    start = begin
    finish = begin + datetime.timedelta(span - 1)
    while start <= end:
        date_ranges.append(date_to_str(start, finish))
        start += datetime.timedelta(span)
        finish += datetime.timedelta(span)
    return date_ranges


def daterange_to_filename(date_range):
    return date_range.replace('.', '')


if __name__ == '__main__':
    # make_default_daterange()
    convert_to_datetime('08.12.2016-08.12.2017')

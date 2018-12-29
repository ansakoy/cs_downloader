import os
import json
import datetime
from pprint import pprint

STATS_FILE = 'stats.json'
PATH = os.path.join(os.getcwd(), STATS_FILE)

# ПОЛЯ СТАТИСТИКИ
TOTAL = 'total'
BY_YEAR = 'byYear'
BY_MONTH = 'byMonth'
BY_DAY = 'byDay'
FULL_TOTAL = 'fullTotal'
FULL_BY_YEAR = 'fullByYear'
FULL_BY_DAY = 'fullByDay'


def load_stats():
    result = None
    if not os.path.exists(PATH):
        return
    try:
        with open(PATH, 'r', encoding='utf-8') as handler:
            result = json.load(handler)
    except Exception as e:
        print(e)
    return result


def dump_stats(data):
    with open(PATH, 'w', encoding='utf-8') as handler:
        json.dump(data, handler, ensure_ascii=False, sort_keys=True, indent=2)


def upd_stats(full=False):
    stats = load_stats()
    date = datetime.date.today()
    year = str(date.year)
    month = str(date.month)
    day = str(date)
    if not stats:
        stats = {
            TOTAL: 0,
            BY_YEAR: dict(),
            BY_DAY: dict(),
            FULL_TOTAL: 0,
            FULL_BY_YEAR: dict(),
            FULL_BY_DAY: dict()
        }
    if full:
        stats[FULL_TOTAL] += 1
        if stats[FULL_BY_YEAR].get(year):
            stats[FULL_BY_YEAR][year][TOTAL] += 1
        else:
            stats[FULL_BY_YEAR][year] = {TOTAL: 1,
                                         BY_MONTH: dict()}
        if stats[FULL_BY_YEAR][year][BY_MONTH].get(month):
            stats[FULL_BY_YEAR][year][BY_MONTH][month] += 1
        else:
            stats[FULL_BY_YEAR][year][BY_MONTH][month] = 1
        if stats[FULL_BY_DAY].get(day):
            stats[FULL_BY_DAY][day] += 1
        else:
            stats[FULL_BY_DAY][day] = 1
        dump_stats(stats)
    else:
        stats[TOTAL] += 1
        if stats[BY_YEAR].get(year):
            stats[BY_YEAR][year][TOTAL] += 1
        else:
            stats[BY_YEAR][year] = {TOTAL: 1,
                                    BY_MONTH: dict()}
        if stats[BY_YEAR][year][BY_MONTH].get(month):
            stats[BY_YEAR][year][BY_MONTH][month] += 1
        else:
            stats[BY_YEAR][year][BY_MONTH][month] = 1
        if stats[BY_DAY].get(day):
            stats[BY_DAY][day] += 1
        else:
            stats[BY_DAY][day] = 1
    dump_stats(stats)


def show_stats():
    text = ''
    stats = load_stats()
    if not stats:
        return 'Статистики пока нет.'
    text += 'Общее число запросов: {}\n'.format(stats[TOTAL])
    text += 'Число завершенных запросов: {} ({}%)\n'.format(stats[FULL_TOTAL],
                                                                     round(stats[FULL_TOTAL] / stats[TOTAL] * 100))
    text += 'Среднее число запросов в день: {}\n'.format(round(stats[TOTAL] / len(stats[BY_DAY])))
    most_frequent = sort_dict(stats[BY_DAY])[0]
    most_frequent_day = most_frequent[0]
    num_queries = most_frequent[1]
    text += 'Наибольшее число запросов ({}) было {}\n'.format(num_queries, most_frequent_day)
    if len(stats[FULL_BY_DAY]):
        full_most_frequent = sort_dict(stats[FULL_BY_DAY])[0]
        full_most_frequent_day = full_most_frequent[0]
        full_num_queries = full_most_frequent[1]
        text += 'Наибольшее число завершенных запросов ({}) было {}\n'.format(full_num_queries, full_most_frequent_day)
    return text


def sort_dict(dictionary):
    items = list(dictionary.items())
    items.sort(key=lambda x:x[1], reverse=True)
    return items


if __name__ == '__main__':
    dict1 = {
        '1': {
            TOTAL: 10,
            BY_DAY: 4
        },
        '2': {
            TOTAL: 20,
            BY_DAY: 7
        },
        '3': {
            TOTAL: 12,
            BY_DAY: 6
        }
    }
    dict2 = {
        '1': 9,
        '2': 3,
        '3': 10,
        '4': 5,
        '5': 10
    }
    # sort_values(dict1, BY_DAY)
    pprint(sort_dict(dict2))





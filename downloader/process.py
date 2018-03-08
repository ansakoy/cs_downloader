'''
Модуль, отвечающий за процесс обработки задачи в части подключения к API
'''

import csv
import json
import os
import requests
import math
import time

import downloader.daterange_processor as drp
from downloader.api_builder import SEARCH, SELECT
from downloader.write_file import JsonWriter, CsvWriter, XlsxWriter
from downloader.extract import *
import downloader.settings as settings

# import daterange_processor as drp
# from api_builder import SEARCH, SELECT
# # from write_file import JsonWriter, CsvWriter, XlsxWriter
# from extract import *

DEFAULT_PARAMS = {'customerregion': '77',
                  'daterange': drp.date_to_str(drp.get_default_daterange()[0],
                                               drp.get_default_daterange()[1]),
                  'fz': '44'}

DEFAULT_CSV = 'downloader/contr_params.csv'
DEFAULT_JSON = 'downloader/contr_params.json'

# os.chdir('CS_DOWNLOADER\cs_downloader\downloader')

LIMIT = 500
BY_CONTRACT = 'BY_CONTRACT'
BY_PRODUCT = 'BY_PRODUCT'

HEADERS_PRODUCT = [CLEARSPENDING_URL, REGNUM, SIGN_DATE,
                   PRODUCT_DESCR, OKPD2, OKPD2_NAME, OKPD, OKPD_NAME, OKDP, OKDP_NAME,
                   SINGLE_PRICE, OKEI, PRODUCT_SUM, QUANTITY,
                   CUSTOMER_NAME, CUSTOMER_INN, CUSTOMER_KPP,
                   FST_SUPP_NAME, FST_SUPP_INN, FST_SUPP_KPP, NUM_SUPPS,
                   CONTRACT_PRICE,
                   CURRENCY, REGION_NAME, CONTRACT_STAGE, FZ]
HEADERS_CONTRACT = [CLEARSPENDING_URL, REGNUM, SIGN_DATE,
                    FST_PROD_DESCR, NUM_PRODUCTS,
                    CUSTOMER_NAME, CUSTOMER_INN, CUSTOMER_KPP,
                    FST_SUPP_NAME, FST_SUPP_INN, FST_SUPP_KPP, NUM_SUPPS,
                    CONTRACT_PRICE,
                    CURRENCY, REGION_NAME, CONTRACT_STAGE, FZ]

HEADERS = {BY_CONTRACT: HEADERS_CONTRACT,
           BY_PRODUCT: HEADERS_PRODUCT}


def get_params_from_csv(source):
    '''
    Загрузить параметры запроса из файла CSV
    Возвращает словарь, содержащий только поля с заполненными значениями.
    Если скрипт не находит файла, то возвращает предупреждение.
    '''
    alert = 'Не могу найти файл CSV с параметрами: {}'.format(source)
    params_dict = dict()
    try:
        with open(source, 'r', encoding='utf-8') as handler:
            reader = csv.reader(handler)
            for row in reader:
                descr, param, val = row
                if len(val) > 0:
                    params_dict[param] = val
        return params_dict
    except FileNotFoundError:
        return alert


# def make_default_json_from_csv():
#     params_dict = dict()
#     with open(DEFAULT_CSV, 'r', encoding='utf-8') as handler:
#         reader = csv.reader(handler)
#         for row in reader:
#             descr, param, val = row
#             if len(val) < 1:
#                 params_dict[param] = None
#             else:
#                 params_dict[param] = val
#     with open(DEFAULT_JSON, 'w') as handler:
#         json.dump(params_dict, handler)


def get_response_from_api(url):
    '''
    Проверка ответа API на заданный запрос.
    Возвращает словарь/список, если запрос прошел успешно.
    Возвращает указание на проблему в виже str, если запрос не удался
    '''
    try:
        response = requests.get(url)
        if response.status_code < 400:
            return response.json()
        elif response.status_code < 500:
            print(response.status_code)
            return 'По этому запросу контрактов не найдено. Попробуйте задать другие параметры.'
        else:
            print(response.status_code)
            print(url)
            alert = '''Ошибка на сервере.\n
            Попробуйте еще раз или обратитесь в поддержку проекта
            "Госзатраты" (https://clearspending.ru/).'''
            return alert
    except requests.exceptions.ConnectionError:
        return 'Проблема с соединением. Возможно, некорректный URL запроса.'


def get_num_pages(api_query):
    '''
    Определить число страниц в выдаче
    '''
    response = get_response_from_api(api_query)
    if type(response) is not str:
        data = response['contracts']
        num_contracts = data['total']
        per_page = data['perpage']
        return math.ceil(num_contracts / per_page)
    return response


def all_in_one(url):
    '''
    Проверить, укладывается число полученных в выдаче контрактов
    в пределы LIMIT.
    Возвращает True, если да, False, если нет, и сообщает об ошибке,
    если она возвращается в ответ на запрос вместо выдачи.
    '''
    response = get_response_from_api(url)
    if type(response) is not str:
        num_contracts = response['contracts']['total']
        if num_contracts < LIMIT:
            return True
        else:
            return False
    return response


def select_writer(out_format, out_name, date_for_name, task):
    '''
    Инициировать объекты классов, записывающих файлы,
    в зависимости от формата (out_format) и типа задачи.
    '''
    if out_format == 'CSV':
        return CsvWriter(date_for_name, HEADERS[task], out_name)
    elif out_format == 'XLSX':
        return XlsxWriter(date_for_name, HEADERS[task], out_name)
    elif out_format == 'JSON':
        return JsonWriter(date_for_name, out_name)
    else:
        return 'Укажите корректный формат: CSV, XLSX или JSON'


def extract_data(api_query, drange, strategy, out_format, out_name, span, task):
    '''
    Выгрузить данные по запросу и записать их в файл
    '''
    url_all_period = api_query + '&daterange={}'.format(drange)
    # print(url_all_period)
    date_for_name = drange.replace('.', '')
    few_contracts = all_in_one(url_all_period)
    if type(few_contracts) is not bool:
        return few_contracts
    if strategy == SELECT or few_contracts:
        num_pages = get_num_pages(url_all_period)
        if type(num_pages) is not int:
            return num_pages
        writer = select_writer(out_format, out_name, date_for_name, task)
        if type(writer) is str:
            return writer
        writer.start()
        for page in range(1, num_pages + 1):
            query = url_all_period + '&page={}'.format(page)
            response = get_response_from_api(query)
            if type(response) is not str:
                contracts = response['contracts']['data']
                for contract in contracts:
                    if out_format == 'JSON':
                        writer.write(contract)
                    else:
                        if task == BY_CONTRACT:
                            writer.write(by_contract(contract))
                        else:
                            products = by_product(contract)
                            for product in products:
                                writer.write(product)
                time.sleep(2)
            else:
                writer.stop()
                return response
        writer.stop()
        print(settings.DONE_MSG.format(writer.get_outpath()))
        return settings.DONE_MSG.format('')
    begin, end = drp.str_to_date(drange)
    ranges = drp.split_daterange(begin, end, span)
    too_many = 0
    base_url = api_query + '&daterange={}'
    writer = select_writer(out_format, out_name, date_for_name, task)
    if type(writer) is str:
        return writer
    writer.start()
    for period in ranges:
        url = base_url.format(period)
        num_pages = get_num_pages(url)
        if num_pages == 'По этому запросу контрактов не найдено. Попробуйте задать другие параметры.':
            continue
        elif type(num_pages) is not int:
            writer.stop()
            return num_pages
        num_contracts_ok = all_in_one(url)
        if type(num_contracts_ok) is bool and not num_contracts_ok:
            too_many += 1
        for page in range(1, num_pages + 1):
            query = url + '&page={}'.format(page)
            response = get_response_from_api(query)
            if type(response) is str:
                writer.stop()
                return response
            contracts = response['contracts']['data']
            for contract in contracts:
                if out_format == 'JSON':
                    writer.write(contract)
                else:
                    if task == BY_CONTRACT:
                        writer.write(by_contract(contract))
                    else:
                        products = by_product(contract)
                        if products:
                            for product in products:
                                writer.write(product)
            time.sleep(2)
    writer.stop()
    alert = ''
    if too_many > 0:
        alert = '''\n
        По этому запросу установлено искусственное ограничение на выдачу: не более 500 контрактов. Мы попытались раздробить запрос на части, разбив заданный временной диапазон на периоды по {} дней. Но для некоторых периодов число контрактов в выдаче все равно достигало 500. Чтобы обогнуть ограничение, вы можете указать более короткий период дробления по временному дипапзону или использовать дополнительные параметры фильтрации (например, по региону заказчика или по ценовому диапазону).'''.format(span)
    print(settings.DONE_MSG.format(writer.get_outpath()))
    return settings.DONE_MSG.format('')


def get_query_info(api_query, drange, strategy, span):
    url_all_period = api_query + '&daterange={}'.format(drange)
    date_for_name = drange.replace('.', '')
    few_contracts = all_in_one(url_all_period)
    if type(few_contracts) is not bool:
        return few_contracts
    if strategy == SELECT or few_contracts:
        response = get_response_from_api(url_all_period)
        if type(response) is not str:
            num_contracts = response['contracts']['total']
            text = 'Найдено контрактов по запросу: {}'.format(num_contracts)
            text += '\nОжидаемое время выгрузки: около {} минут(ы)'.format(round(num_contracts / 1000.0))
            return text
        return response
    begin, end = drp.str_to_date(drange)
    ranges = drp.split_daterange(begin, end, span)
    num_contracts = 0
    too_many = 0
    base_url = api_query + '&daterange={}'
    for period in ranges:
        url = base_url.format(period)
        # print(url)
        response = get_response_from_api(url)
        if response == 'По этому запросу контрактов не найдено. Попробуйте задать другие параметры.':
            continue
        elif type(response) is str:
            return response
        total = response['contracts']['total']
        if total >= LIMIT:
            too_many += 1
        num_contracts += total
    text = 'Найдено контрактов по запросу: {}\n'.format(num_contracts)
    text += '\nОжидаемое время выгрузки: около {} минут(ы)'.format(round(num_contracts / 1000.0))
    print(text)
    alert = ''
    if too_many > 0:
        alert = '''\n
        По этому запросу установлено искусственное ограничение на выдачу: не более 500 контрактов. Мы попытались раздробить запрос на части, разбив заданный временной диапазон на периоды по {} дней. Но для некоторых периодов число контрактов в выдаче все равно достигало 500. Чтобы обогнуть ограничение, вы можете указать более короткий период дробления по временному дипапзону или использовать дополнительные параметры фильтрации (например, по региону заказчика или по ценовому диапазону).'''.format(span)
    return text + alert


if __name__ == '__main__':
    # API = 'http://openapi.clearspendng.ru/restapi/v3/contracts/select/?&customerregion=77&currentstage=E&daterange=01.01.2017-01.03.2017&fz=44'
    # get_num_pages(API)
    print(get_params_from_csv(DEFAULT_CSV))

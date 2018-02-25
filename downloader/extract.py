# -*- coding: utf-8 -*-

'''
Модуль для извлечения определенных значений из документов, получаемых
по запросу.
'''

import json


# Поля выгружаемых таблиц
CLEARSPENDING_URL = 'clearspending_url' # ссылка на карточку контракта на clearspending.ru
SIGN_DATE = 'sign_date' # дата подписания контракта
PRODUCT_DESCR = 'product_description' # описание закупленного продукта
FST_PROD_DESCR = '1st_product_description' # описание первого продукта (при выгрузке по контрактам)
NUM_PRODUCTS = 'num_products' # число продуктов в контракте (при выгрузке по контрактам)
OKPD2 = 'okpd2' # код ОКПД2 (если имеется)
OKPD2_NAME = 'okpd2_name' # расшифровка кода ОКПД2 (если имеется)
OKPD = 'okpd' # код ОКПД (если имеется)
OKPD_NAME = 'okpd_name' # расшифровка кода ОКПД (если имеется)
OKDP = 'okdp' # код ОКДП (если имеется), актуально до 2014 г.
OKDP_NAME = 'okdp_name' # расшифровка кода (если имеется), актуально до 2014 г.
SINGLE_PRICE = 'single_price' # цена за единицу продукта
OKEI = 'okei' # единица измерения
PRODUCT_SUM = 'product_sum' # сумма по продукту
QUANTITY = 'quantity' # количество закупленных единиц
CONTRACT_PRICE = 'contract_price' # сумма всего контракта
CURRENCY = 'currency' # валюта
REGION_NAME = 'region_name' # наименование региона
REGNUM = 'regnum' # реестровый номер контракта
CUSTOMER_NAME = 'customer_name' # наименование заказчика
CUSTOMER_INN = 'customer_inn' # ИНН заказчика
CUSTOMER_KPP = 'customer_kpp' # КПП заказчика
FST_SUPP_NAME = '1st_supp_name' # наименование первого поставщика
FST_SUPP_INN = '1st_supp_inn' # ИНН первого поставщика
FST_SUPP_KPP = '1st_supp_kpp' # КПП первого поставщика
NUM_SUPPS = 'num_suppliers' # всего поставщиков
CONTRACT_STAGE = 'contract_stage' # стадия исполнения контракта (актуально только для 44-ФЗ)
FZ = 'fz' # федеральный закон - 44-ФЗ, 223-ФЗ, до 2014 г. 94-ФЗ


REGIONS_REFERENCE = 'downloader/region_codes.json'

CONTRACT_STAGES_MAP = {'E': 'Исполнение',
          'EC': 'Исполнение завершено',
          'ET': 'Исполнение прекращено'}


def load_json(source_file):
    '''
    Загрузить файл JSON
    '''
    with open(source_file, 'r') as handler:
        return json.load(handler)


def by_contract(contract):
    '''
    Собрать данные для выгрузки по контрактам
    '''
    region_codes = load_json(REGIONS_REFERENCE)
    regnum = contract.get('regNum', '-')
    base_url = 'https://clearspending.ru/contract/{}'
    contract_info = {CLEARSPENDING_URL: base_url.format(regnum),
                     REGNUM: regnum,
                     SIGN_DATE: contract.get('signDate', '-'),
                     FZ: contract.get('fz', '-'),
                     CUSTOMER_NAME: contract.get('customer', {}).get('fullName', '-'),
                     CUSTOMER_INN: contract.get('customer', {}).get('inn', '-'),
                     CUSTOMER_KPP: contract.get('customer', {}).get('kpp', '-'),
                     NUM_SUPPS: len(contract.get('suppliers', [])),
                     FST_SUPP_NAME: contract.get('suppliers', [{}])[0].get('organizationName', '-'),
                     FST_SUPP_INN: contract.get('suppliers', [{}])[0].get('inn', '-'),
                     FST_SUPP_KPP: contract.get('suppliers', [{}])[0].get('kpp', '-'),
                     CONTRACT_PRICE: contract.get('price', '-'),
                     CURRENCY: contract.get('currency', {}).get('name', '-'),
                     REGION_NAME: region_codes.get(contract.get('regionCode', '-')),
                     CONTRACT_STAGE: CONTRACT_STAGES_MAP.get(contract.get('currentContractStage', '-')),
                     NUM_PRODUCTS: len(contract.get('products', [])),
                     FST_PROD_DESCR: contract.get('products', [{}])[0].get('name', '-')}
    return contract_info


def get_product_details(product, contr_info):
    '''
    Собрать детали по продукту
    '''
    contr_info[PRODUCT_DESCR] = product.get('name', '-')
    contr_info[OKPD2] = product.get('OKPD2', {}).get('code', '-')
    contr_info[OKPD2_NAME] = product.get('OKPD2', {}).get('name', '-')
    contr_info[OKPD] = product.get('OKPD', {}).get('code', '-')
    contr_info[OKPD_NAME] = product.get('OKPD', {}).get('name', '-')
    contr_info[OKDP] = product.get('OKDP', {}).get('code', '-')
    contr_info[OKDP_NAME] = product.get('OKDP', {}).get('name', '-')
    contr_info[SINGLE_PRICE] = product.get('price', '-')
    contr_info[OKEI] = product.get('OKEI', {}).get('name', '-')
    contr_info[QUANTITY] = product.get('quantity', '-')
    contr_info[PRODUCT_SUM] = product.get('sum', '-')
    return contr_info


def by_product(contract):
    '''
    Собрать данные для выгрузки по контрактам
    '''
    region_codes = load_json(REGIONS_REFERENCE)
    regnum = contract.get('regNum', '-')
    base_url = 'https://clearspending.ru/contract/{}'
    all_products = list()
    contract_info = {CLEARSPENDING_URL: base_url.format(regnum),
                     REGNUM: regnum,
                     SIGN_DATE: contract.get('signDate', '-'),
                     FZ: contract.get('fz', '-'),
                     CUSTOMER_NAME: contract.get('customer', {}).get('fullName', '-'),
                     CUSTOMER_INN: contract.get('customer', {}).get('inn', '-'),
                     CUSTOMER_KPP: contract.get('customer', {}).get('kpp', '-'),
                     NUM_SUPPS: len(contract.get('suppliers', [])),
                     FST_SUPP_NAME: contract.get('suppliers', [{}])[0].get('organizationName', '-'),
                     FST_SUPP_INN: contract.get('suppliers', [{}])[0].get('inn', '-'),
                     FST_SUPP_KPP: contract.get('suppliers', [{}])[0].get('kpp', '-'),
                     CONTRACT_PRICE: contract.get('price', '-'),
                     CURRENCY: contract.get('currency', {}).get('name', '-'),
                     REGION_NAME: region_codes.get(contract.get('regionCode', '-')),
                     CONTRACT_STAGE: CONTRACT_STAGES_MAP.get(contract.get('currentContractStage', '-'))}
    products = contract.get('products')
    if products:
        for product in products:
            row = get_product_details(product, contract_info)
            all_products.append(row)
        return all_products

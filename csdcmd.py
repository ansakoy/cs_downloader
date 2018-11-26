import argparse
import launch

parser = argparse.ArgumentParser(description='Configure request')
parser.add_argument('-q', '--query',
                    type=str,
                    metavar='',
                    help='Полный путь к файлу CSV, содержащему параметры запроса')
parser.add_argument('-s', '--span',
                    type=str,
                    metavar='',
                    help='Число дней в подпериодах, на которые нужно раздробить период (по умолчанию 30)')
parser.add_argument('-n', '--name',
                    type=str,
                    metavar='',
                    help='Название файла, в котором нужно сохранить данные, например, "contracts_spb"')
parser.add_argument('-d', '--demo',
                    action='store_true',
                    help='Запустить скрипт в режиме ДЕМО')
extract_options = parser.add_mutually_exclusive_group()
extract_options.add_argument('-c', '--contracts',
                    action='store_true',
                    help='Извлечь данные в режиме "1 строка = 1 контракт"')
extract_options.add_argument('-p', '--products',
                    action='store_true',
                    help='Извлечь данные в режиме "1 строка = 1 продукт"')
format_options = extract_options = parser.add_mutually_exclusive_group()
format_options.add_argument('-x', '--xlsxout',
                    action='store_true',
                    help='Сохранить данные в файле XLSX (по умолчанию - CSV)')
format_options.add_argument('-j', '--jsonout',
                    action='store_true',
                    help='Сохранить данные в файле JSON (по умолчанию - CSV)')

def launch_csd(query, contracts, products, jsonout, xlsxout, name,
                span, demo):
    task = 'INFO'
    if a.contracts:
        task = 'BY_CONTRACT'
    elif a.products:
        task = 'BY_PRODUCT'
    outformat = 'CSV'
    if a.jsonout:
        outformat = 'JSON'
    elif a.xlsxout:
        outformat= 'XLSX'
    span = 30
    if a.span:
        try:
            span = int(a.span)
        except ValueError:
            print('Используйте целочисленные значения для span')
            return
    demo = False
    if a.demo:
        demo = True
    launch.launch(source=query, task=task, out_format=outformat,
            out_name=a.name,
            span=span, demo=demo)


if __name__ == '__main__':
    a = parser.parse_args()
    launch_csd(a.query, a.contracts, a.products, a.xlsxout, a.jsonout, a.name, a.span, a.demo)

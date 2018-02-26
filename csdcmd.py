import argparse
import launch

parser = argparse.ArgumentParser(description='Configure request')
parser.add_argument('-q', '--query',
                    type=str,
                    metavar='',
                    help='Path to CSV file containing query parameters')
parser.add_argument('-s', '--span',
                    type=str,
                    metavar='',
                    help='Number of days in subperiods')
parser.add_argument('-n', '--name',
                    type=str,
                    metavar='',
                    help='Name for output file, e.g. "contracts_spb"')
parser.add_argument('-d', '--demo',
                    action='store_true',
                    help='First segments of OKPD2 code')
extract_options = parser.add_mutually_exclusive_group()
extract_options.add_argument('-c', '--contracts',
                    action='store_true',
                    help='Extract data in "1 line = 1 contract" mode')
extract_options.add_argument('-p', '--products',
                    action='store_true',
                    help='Extract data in "1 line = 1 product" mode')
format_options = extract_options = parser.add_mutually_exclusive_group()
format_options.add_argument('-x', '--xlsxout',
                    action='store_true',
                    help='Store extracted data in XLSX; default: CSV')
format_options.add_argument('-j', '--jsonout',
                    action='store_true',
                    help='Store extracted data in JSON; default: CSV')

def launch_csd(query, contracts, products, jsonout, xlsxout, name,
                span, demo):
    task = 'INFO'
    if a.contracts:
        task = 'BY_CONTRACT'
    elif a.products:
        task = 'BY_PRODUCT'
    outformat = 'CSV'
    if a.jsonout:
        outformat= 'JSON'
    elif a.xlsxout:
        outformat= 'XLSX'
    name = None
    if a.name:
        name = name
    span = 30
    if a.span:
        try:
            span = int(span)
        except ValueError:
            print('Use integer values for span.')
            return
    demo = False
    if a.demo:
        demo = True
    launch.launch(source=query, task=task, out_format=outformat,
            span=span, demo=demo)

if __name__ == '__main__':
    a = parser.parse_args()
    launch_csd(a.query, a.contracts, a.products, a.xlsxout, a.jsonout,
                a.name, a.span, a.demo)

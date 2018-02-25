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
                    metavar='',
                    help='First segments of OKPD2 code')
extract_options = parser.add_mutually_exclusive_group()
extract_options.add_argument('-c', '--contracts',
                    action='store_true',
                    help='Extract data in "1 line = 1 contract" mode')
extract_options.add_argument('-p', '--products',
                    action='store_true',
                    help='Extract data in "1 line = 1 product" mode')
format_options = extract_options = parser.add_mutually_exclusive_group()
format_options.add_argument('-x', '--xlsx',
                    action='store_true',
                    help='Store extracted data in XLSX; default: CSV')
format_options.add_argument('-j', '--json',
                    action='store_true',
                    help='Store extracted data in JSON; default: CSV')

def launch_csd(params_source, task, outformat, out_name, span, demo):
    if not a.daterange:
        daterange = dp.default_period()
    period = dp.convert_date(daterange)
    if a.okpd or a.okpd2 or a.okpd_cat or a.okpd2_cat:
        if a.daterange:
            analyst = CSProduct(start_stop=daterange,
                                okpd=okpd,
                                okpd2=okpd2,
                                okpd_cat=okpd_cat,
                                okpd2_cat=okpd2_cat)
        else:
            analyst = CSProduct(okpd=okpd,
                                okpd2=okpd2,
                                okpd_cat=okpd_cat,
                                okpd2_cat=okpd2_cat)
        analyst.product_launcher()
        if a.mail:
            begin = dp.to_unicode(period[0])
            end = dp.to_unicode(period[1])
            subject = analyst.filename
            text = 'Дата и время выгрузки: {}-{}'.format(begin, end)
            fname = analyst.filename + '.xlsx'
            send_email(subject, fname, text, email)
    else:
        if a.daterange:
            analyst = CSAnalyst(start_stop=period)
        elif a.numdays:
            analyst = CSAnalyst(period=period)
        else:
            analyst = CSAnalyst()
        analyst.standard_launcher()
        if a.mail:
            subject = analyst.filename
            text = 'Дата и время выгрузки: {}'.format(datetime.datetime.now()).encode('utf-8')
            fname = 'data/' + analyst.filename + '.xlsx'
            send_email(subject, fname, text, email)
if __name__ == '__main__':
    a = parser.parse_args()
    launch_csd(a.query, a.span, outformat, out_name, span, demo)

'''
Модуль для записи разных типов файлов (JSON, CSV, XLSX)
'''

import csv
import json
import os
from openpyxl import Workbook
import downloader.settings as settings


# parent = os.path.normpath(os.getcwd() + os.sep + os.pardir)
PATH = os.path.join(os.getcwd(), 'data')
DEFAULT_FNAME = 'contracts_{}'

class JsonWriter():

    def __init__(self, daterange, outputname=None):
        if outputname is None:
            self.fname = os.path.join(PATH, DEFAULT_FNAME.format(daterange) + '.json')
        else:
            self.fname = os.path.join(PATH, outputname + '.json')
        settings.OUTPUT_PATH += self.fname
        self.first = True
        self.handler = None

    def start(self):
        self.handler = open(self.fname, 'w')
        self.handler.write('[')

    def write(self, dictionary):
        if not self.first:
            self.handler.write('\n')
        json.dump(dictionary, self.handler)
        self.first = False

    def stop(self):
        self.handler.write(']')
        self.handler.close()


class CsvWriter():

    def __init__(self, daterange, headers, outputname=None):
        if outputname is None:
            self.fname = os.path.join(PATH, DEFAULT_FNAME.format(daterange) + '.csv')
        else:
            self.fname = os.path.join(PATH, outputname + '.csv')
        settings.OUTPUT_PATH += self.fname
        self.writer = None
        self.handler = None
        self.headers = headers

    def start(self):
        self.handler = open(self.fname, 'w', encoding='utf-8', newline='')
        self.writer = csv.DictWriter(self.handler, fieldnames=self.headers)
        self.writer.writeheader()

    def write(self, dictionary):
        self.writer.writerow(dictionary)

    def stop(self):
        self.handler.close()


class XlsxWriter():

    def __init__(self, daterange, headers, outputname=None):
        if outputname is None:
            self.fname = os.path.join(PATH, DEFAULT_FNAME.format(daterange) + '.xlsx')
        else:
            self.fname = os.path.join(PATH, outputname + '.xlsx')
        settings.OUTPUT_PATH += self.fname
        self.handler = None
        self.sheet = None
        self.headers = headers

    def start(self):
        self.handler = Workbook()
        self.sheet = self.handler.active
        self.sheet.append(self.headers)

    def make_row(self, dictionary):
        row = list()
        for field in self.headers:
            row.append(dictionary[field])
        return row

    def write(self, dictionary):
        row = self.make_row(dictionary)
        self.sheet.append(row)

    def stop(self):
        self.handler.save(filename=self.fname)


if __name__ == '__main__':
    pass

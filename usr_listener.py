import time
import os
from sys import argv

def main():
    usrdata = os.listdir('usrdata')
    if len(usrdata):
        print(usrdata)
        for fname in usrdata:
            print('NEW FILE')
            os.system('python emailscript.py fname')
            os.remove(os.path.join('usrdata', fname))
            print(usrdata)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(5)

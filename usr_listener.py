import time
import os

def main():
    usrdata = os.listdir('usrdata')
    if len(usrdata):
        print(usrdata)
        for fname in usrdata:
            path = os.path.join('usrdata', fname)
            os.system('python emailscript.py {}'.format(path))


if __name__ == '__main__':
    while True:
        main()
        time.sleep(5)

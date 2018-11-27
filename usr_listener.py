import time
import os
import sys


def write_pid():
    pid_fname = '{}_{}.pid'.format(os.path.splitext(os.path.basename(sys.argv[0]))[0], str(os.getpid()))
    with open(pid_fname, 'w') as handler:
        handler.write(str())


def main():
    usrdata = os.listdir('usrdata')
    if len(usrdata):
        print(usrdata)
        for fname in usrdata:
            path = os.path.join('usrdata', fname)
            os.system('python emailscript.py {}'.format(path))


if __name__ == '__main__':
    write_pid()
    while True:
        main()
        time.sleep(5)

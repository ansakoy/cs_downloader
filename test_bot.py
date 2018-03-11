import time
from sys import argv


def test_bot(sleep):
    time.sleep(int(sleep))
    message = 'slept for %s seconds' % sleep
    print(message)


if __name__ == '__main__':
    test_bot(argv[1])

# coding:utf-8


import signal
import sys

import logging
import time
import getopt


# http://www.python-izm.com/contents/basis/import.shtml
# https://github.com/aws/aws-iot-device-sdk-python


def cleanup(*args):
    sys.exit(0)


# inputがtargetsに含まれているかを確認する。
def contains(input, targets):
    #    sysout(targets)
    flag = False
    for target in targets:
        if (input == target):
            flag = True
    return flag


# flushしないと出力されないケースがあるため、必ずflushするprint文
def sysout(message):
    print(message)
    sys.stdout.flush()







# 以下未使用。
def main(args):
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    #sendMessage('kino')

    while True:
        time.sleep(10)


if __name__ == '__main__':
    # http://www.python-izm.com/contents/basis/command_line_arguments.shtml
    # sysout(args[0])
    # sysout(args[1]) でアクセス出来るが、args[0]はプログラム名。
    main(sys.argv)

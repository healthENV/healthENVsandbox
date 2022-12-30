#!/usr/bin/env python3

import time
import signal
import os

from multiprocessing import Process

from flask import Flask, jsonify

STOP_TIMEOUT = int(os.environ.get('STOP_TIMEOUT', '10'))
PORT = int(os.environ.get('PORT', '8000'))

APP = Flask(__name__)



def date_Time(message):
    now = datetime.now()
    dateTime = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"{ dateTime } - { message }")
    f = open("closeDownInfo.txt", "a")
    f.write(f"{ dateTime } - { message }\n")
    f.close()


@APP.route('/')
def home():
    return jsonify(**{'status': 'ok'}), 200


def run():
    APP.run(host='0.0.0.0', port=PORT)


def signal_handler(sig, _frame):
    """Handling the SIGTERM event"""
    date_Time("Closing down routine")
    print(f'Received signal {sig} - stopping gracefully')
    count = STOP_TIMEOUT
    while count > 0:
        print(f'cleaning up: {count}')
        time.sleep(1)
        count -= 1
    print('Finished cleanup...')


def main():
    # Create a process and pipe to pass messages to the process.
    process = Process(target=run)
    process.start()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()
    process.join()


if __name__ == "__main__":
    main()
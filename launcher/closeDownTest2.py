#!/usr/bin/env python3
"""
    Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
    Licensed under the Apache License, Version 2.0 (the "License").
    You may not use this file except in compliance with the License.
    A copy of the License is located at
        http://www.apache.org/licenses/LICENSE-2.0
    or in the "license" file accompanying this file. This file is distributed
    on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
    express or implied. See the License for the specific language governing
    permissions and limitations under the License.
"""
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
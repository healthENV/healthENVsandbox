import signal
from datetime import datetime

def date_Time(message):
    now = datetime.now()
    dateTime = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"{ dateTime } - { message }")
    f = open("closeDownInfo.txt", "a")
    f.write(f"{ dateTime } - { message }\n")
    f.close()

run = True

def handler_stop_signals(signum, frame):
    date_Time("Closing down routine")
    global run
    run = False

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)



if __name__ == "__main__":
    print("Hello from inside the launcher Docker container")
    date_Time("Start up")
    
    while run:
        pass # do stuff including other IO stuff
    
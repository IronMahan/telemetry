import serial
import json
import csv
import datetime
import time
import threading
import serial.tools.list_ports as list_ports

settings = {
    "Port": None,
    "plot_size": None,
    "baudrate": None,
    "plotinfo": None
}


def getPortList():
    ports = list_ports.comports()
    if not ports:
        print("No Port found")
    else:
        for port in ports:
            print(port)



def config():
    # Read config.json
    while True:
        try:
            inp = input("Press ENTER to use default config.json path or enter the path: ")
            if inp == '':    
                with open("config.json", "r") as conf:
                    f = json.load(conf)
                    settings["baudrate"]  = f['settings']['baudrate']
                    settings["plot_size"] = f['settings']['plot_size']
                    settings["plotinfo"]  = f['settings']['data']

                    com = input("Enter Port COM")
                    settings["Port"] = 'COM' + com
                
                print(json.dumps(settings, indent=4))

            elif inp == 'q':
                return 0
            else:
                print("Try again! File not found!")
            
        except:
            print("Failed to load config.json\nTRY AGAIN\n\n")

def readData():
    global serialData
    with open(str(datetime.datetime.now()) + '.csv', 'a', newline='') as log:
        initTime = time.time()
        logger = csv.writer(log)
        while True:
            line = serialInst.readline().decode("utf-8").strip()
            if line:
                with lock:
                    serialData = f"{line},{str(time.time() - initTime)}"
            logger.writerow(eval(serialData))
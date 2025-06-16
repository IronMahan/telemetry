import json
import datetime
import csv
import serial
import os
import time
import inquirer

import numpy as np
import matplotlib.pyplot as plt
import serial.tools.list_ports as list_ports

from pyfiglet import Figlet
from tabulate import tabulate
from matplotlib.animation import FuncAnimation

    
class App:
    def __init__(self):
        self.outputDir = None
        self.port = None
        self.baudrate = None
        self.serialStatus = False
        self.settings = self.readSettings()
        self.avalablePorts = self.getPorts()
        self.serialInst = serial.Serial(timeout=1)
        self.heading = Figlet(font='slant').renderText("FLARE")
        self.headers = ["TITLE", "STATUS"]
    
    
    # Main functions
    
    def listPorts(self):
        for port in myApp.avalablePorts:
            print(f" > {port}")

    def selectBaudRate(self):
        question = [inquirer.List('baud',
                                  message="Select Baud rate",
                                  choices=[300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 31250, 38400, 57600,115200])]
        self.baudrate = inquirer.prompt(question)['baud']

    def selectPort(self):
        print("Connected ports\n")
        self.listPorts()
        input("\nConnect the arduino and then press ENTER\n")

        # Update the available ports 
        self.avalablePorts = self.getPorts()
        
        # Select the port 
        port = [inquirer.List('port',
                    message="Select the port",
                    choices=self.avalablePorts),
                    ]
        self.port = inquirer.prompt(port)['port']
        self.connectPort()
    

    def connectPort(self):
        if self.serialStatus == True:
            self.serialInst.close()
            self.serialStatus = False

        self.serialInst.baudrate = self.baudrate
        self.serialInst.port = self.port
        self.serialInst.open()
        self.serialStatus = True
    
    def readData(self):
        while True:
            #read data from serial port
            data = self.serialInst.readline()

            #if there is smth do smth
            if len(data) >= 1:
                return eval(data.decode())
        
    def clearScreen(self):  # Clears and refreshes the screen
        os.system('cls' if os.name == 'nt' else 'clear')
        table = [["Baud Rate", self.baudrate], 
                 ["COM Port", self.port],
                 ["Port Status", self.serialStatus],
                 ["No. of graphs", self.settings['rows'] * self.settings['cols']]]
        # print(self.settings, "hhh")
        print(self.heading)
        print("Flight Logging and Remote Evaluation software\n")
        print(tabulate(table, self.headers, tablefmt="double_grid"))
    

    @staticmethod
    def getPorts():
        ports = list_ports.comports()
        return [port.device for port in ports] # to get the o/p as [COM4, COM5, ...]

    @staticmethod
    def readSettings():
        with open("settings.json") as f:
            out = json.load(f)
        return out

    @staticmethod
    def showError(error):
        print(error)
        input("Press ENTER")


if __name__ == '__main__':
    myApp = App()

    userChoices = ["Edit configuration", "Refresh", "RUN", "EXIT"]
    editOptions = ["Baud rate", "COM", "EXIT"]

    DATA = None
    RUN = True

    myApp.clearScreen()

    # INITIALISE
    myApp.selectBaudRate()
    myApp.clearScreen()
    myApp.selectPort()

    while RUN:
        try:
            # time.sleep(5)
            myApp.clearScreen()
            userChoice = [inquirer.List('userInp',
                            message="SELECT",
                            choices=userChoices),
                    ]
            choice = inquirer.prompt(userChoice)['userInp']
            match choice:
                # ["Edit configuration", "Refresh", "RUN"]
                case "Edit configuration":
                    editChoice = [inquirer.List('userInp',
                            message="SELECT",
                            choices=editOptions),
                    ]
                    choice = inquirer.prompt(editChoice)['userInp']
                    
                    if choice == editOptions[0]:
                        myApp.selectBaudRate()
                        
                    elif choice == editOptions[1]:
                        myApp.avalablePorts = myApp.getPorts()
                        myApp.selectPort()

                    else:
                        pass
                
                case "Refresh":
                    myApp.connectPort()
                    myApp.settings = myApp.readSettings()

                case "RUN":
                    if myApp.serialStatus == True:

                        TIME_INCRIMENT = 5

                        x = []
                        y = [[] for _ in range(myApp.settings['rows']*myApp.settings['cols'])]

                        # outputFile = f"{datetime.datetime.now()}.csv"
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        outputFile = f"{timestamp}.csv"
                        with open(outputFile, 'w', newline='') as f: 
                            myWriter = csv.writer(f, delimiter=',')

                            fig, ax = plt.subplots(nrows=myApp.settings["rows"],
                                                   ncols=myApp.settings["cols"],
                                                   figsize=(9, 5))

                            lines = []
                            if isinstance(ax, np.ndarray):
                                ax = ax.flat
                            else:
                                ax = [ax]

                            for name, idx in list(myApp.settings["axis"].items()):
                                line, = ax[idx].plot([], [])
                                ax[idx].set_xlim(0, TIME_INCRIMENT)
                                ax[idx].set_ylim(*list(myApp.settings['ylim'].values())[idx])
                                ax[idx].set_xlabel("Time(s)")
                                ax[idx].set_ylabel(name)
                                lines.append(line)

                            def update(frame):
                                global TIME_INCRIMENT
                                # print("Hello")
                                x.append(time.time() - init_time)
                                DATA = myApp.readData()
                                # print(DATA)
                                myWriter.writerow([*DATA, x[-1]])
                                # rescale = False

                                # val -> data position, idx -> axis
                                for val, idx in list(zip(myApp.settings["vals"].values(),
                                                        myApp.settings["axis"].values())):

                                    y[idx].append(DATA[val])
                                    lines[idx].set_data(x, y[idx])

                                    if x[-1] >= TIME_INCRIMENT:
                                        TIME_INCRIMENT += 5
                                        for i in range(myApp.settings["cols"] * myApp.settings["rows"]):
                                            ax[i].set_xlim(ax[i].get_xlim()[0], TIME_INCRIMENT)
                                        fig.canvas.draw()

                                    if y[idx][-1] > ax[idx].get_ylim()[1]:
                                        ax[idx].set_ylim(ax[idx].get_ylim()[0], ax[idx].get_ylim()[1] + 100)
                                        fig.canvas.draw()

                                return lines
                                    
                            init_time = time.time()
                            ani = FuncAnimation(fig, update, frames=range(1, 500_000_000), blit=True, interval=10, repeat=False)
                            plt.show()
                case "EXIT":
                    ext = input("Do you want to exit[Y/n]").lower()
                    if ext == 'y':
                        RUN = False

        except Exception as e:
            myApp.serialInst.close()
            myApp.showError(e)
        

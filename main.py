import serial.tools.list_ports as list_ports

def getPortList():
    ports = list_ports.comports()
    if not ports:
        return None
    return ports

def connect(port)
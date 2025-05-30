from serial.tools import list_ports

def find_makcu_port():
    for port in list_ports.comports():
        if "CH343" in port.description:
            return port.device
    return None
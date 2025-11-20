import serial.tools.list_ports

def list_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Port: {port.device} - {port.description}")

if __name__ == "__main__":
    list_ports()
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"Port: {port.device} - {port.description}")


# SMS port orqali test qilip jo'natish
# import serial
#
# port = "COM8"
# try:
#     ser = serial.Serial(port, baudrate=115200, timeout=5)
#     ser.write(b'AT\r')
#     response = ser.read(64)
#     print(response.decode())
#     ser.close()
# except Exception as e:
#     print(f"Xatolik: {e}")

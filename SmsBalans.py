from gsmmodem.modem import GsmModem

# Modem COM portini ko'rsatish
PORT = 'COM18'  # Windows uchun (masalan, COM3, COM4)
# PORT = '/dev/ttyUSB0'  # Linux/Mac uchun
# BAUDRATE = 9600  # USB modem odatda 9600 baud tezlikda ishlaydi
BAUDRATE = 115200

# Modemni ulash
modem = GsmModem(PORT, BAUDRATE)
modem.connect()  # Modem bilan ulanish

# USSD kodini jo‘natish (Misol uchun, UzMobile va Ucell uchun *100#)
ussd_code = "*108#"
response = modem.sendUssd(ussd_code)

print(f"📊 Balans ma'lumoti: {response}")

modem.close()  # Modemni o'chirish

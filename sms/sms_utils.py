import serial
import time
import serial.tools.list_ports

def get_modem_sms_port():
    """ SMS jo‘natish uchun to‘g‘ri COM portni aniqlash """
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Proprietary USB Modem" in port.description or "Diagnostics Interface" in port.description:
            print(f"✅ SMS uchun ishlatiladigan port: {port.device}")
            return port.device  # Mos keladigan portni qaytarish
    print("❌ SMS yuborish uchun mos port topilmadi!")
    return None  # Agar port topilmasa, None qaytariladi

def format_phone_number(phone_number):
    """ Telefon raqamini to‘g‘ri formatga keltirish (+998XXXXXXXXX) """
    phone_number = phone_number.strip()  # Bo‘sh joylarni olib tashlash
    if not phone_number.startswith("+"):  # Agar oldida + belgisi bo‘lmasa, qo‘shish
        phone_number = f"+{phone_number}"
    return phone_number

def send_sms_via_modem(phone_number, message):
    """ USB Modem orqali SMS jo‘natish funksiyasi """
    modem_port = get_modem_sms_port()
    if modem_port is None:
        print("❌ USB modem topilmadi! SMS jo‘natilmadi.")
        return False

    phone_number = format_phone_number(phone_number)  # Telefon raqamini formatlash

    try:
        ser = serial.Serial(modem_port, baudrate=115200, timeout=5)
        time.sleep(1)

        # AT komandalar
        ser.write(b'AT\r')
        time.sleep(1)
        ser.write(b'AT+CMGF=1\r')  # Text rejimiga o'tish
        time.sleep(1)
        ser.write(f'AT+CMGS="{phone_number}"\r'.encode())
        time.sleep(1)
        ser.write(message.encode() + b"\x1A")  # CTRL+Z tugmasi
        time.sleep(3)

        ser.close()
        print(f"✅ SMS muvaffaqiyatli yuborildi: {phone_number}")
        return True  # SMS muvaffaqiyatli jo‘natildi
    except Exception as e:
        print(f"❌ SMS yuborishda xatolik: {e}")
        return False  # SMS jo‘natishda xatolik

# import serial
# import time
# #COM8
# def send_sms(phone_number, message, modem_port="COM12"):
#     """ USB modem orqali SMS jo‘natish """
#     try:
#         # Serial port ochish
#         ser = serial.Serial(modem_port, baudrate=115200, timeout=5)
#         time.sleep(1)
#
#         # AT komandalar yuborish
#         ser.write(b'AT\r')
#         time.sleep(1)
#         ser.write(b'AT+CMGF=1\r')  # Text rejimiga o'tish
#         time.sleep(1)
#         ser.write(f'AT+CMGS="{phone_number}"\r'.encode())
#         time.sleep(1)
#         ser.write(message.encode() + b"\x1A")  # CTRL+Z tugmasi (SMS jo'natish)
#         time.sleep(3)
#
#         ser.close()
#         print(f"✅ SMS yuborildi: {phone_number}")
#         return True
#     except Exception as e:
#         print(f"❌ SMS yuborishda xatolik: {e}")
#         return False
#
# if __name__ == "__main__":
#     phone_number = input("Telefon raqamini kiriting (+998XXXXXXXXX): ").strip()
#     message = input("SMS matnini kiriting: ").strip()
#
#     if send_sms(phone_number, message):
#         print("✅ SMS muvaffaqiyatli jo‘natildi!")
#     else:
#         print("❌ Xatolik yuz berdi, iltimos tekshiring!")

#
# import serial.tools.list_ports
#
# def list_ports():
#     ports = serial.tools.list_ports.comports()
#     for port in ports:
#         print(f"Port: {port.device} - {port.description}")
#
# if __name__ == "__main__":
#     list_ports()


# import serial
# import time
# import textwrap
#
# def send_sms(phone_number, message, modem_port="COM8"):
#     """ USB modem orqali 160+ belgili SMSlarni bo‘lib jo‘natish """
#     try:
#         # Serial port ochish
#         ser = serial.Serial(modem_port, baudrate=115200, timeout=5)
#         time.sleep(1)
#
#         # AT komandalar yuborish
#         ser.write(b'AT\r')
#         time.sleep(1)
#         ser.write(b'AT+CMGF=1\r')  # Text rejimiga o'tish
#         time.sleep(1)
#
#         # Agar SMS uzun bo'lsa, uni bo'lib yuboramiz
#         parts = textwrap.wrap(message, 153)  # Har bir qism 153 belgi bo'ladi
#         total_parts = len(parts)
#
#         for i, part in enumerate(parts, start=1):
#             sms_part = f"{part}"  # Qismlar raqamlari bilan jo‘natiladi
#             print(f"📤 Yuborilmoqda: {sms_part}")
#
#             ser.write(f'AT+CMGS="{phone_number}"\r'.encode())
#             time.sleep(1)
#             ser.write(sms_part.encode() + b"\x1A")  # CTRL+Z tugmasi (SMS jo‘natish)
#             time.sleep(3)  # SMS jo‘natishni kutish
#
#         ser.close()
#         print(f"✅ SMS {total_parts} qismda yuborildi!")
#         return True
#
#     except Exception as e:
#         print(f"❌ SMS yuborishda xatolik: {e}")
#         return False
#
# if __name__ == "__main__":
#     phone_number = input("Telefon raqamini kiriting (+998XXXXXXXXX): ").strip()
#     message = input("SMS matnini kiriting: ").strip()
#
#     if send_sms(phone_number, message):
#         print("✅ SMS muvaffaqiyatli jo‘natildi!")
#     else:
#         print("❌ Xatolik yuz berdi, iltimos tekshiring!")

# Ishladi
#
import serial
import time
import textwrap

def send_sms(phone_number, message, modem_port="COM8"):
    """ USB modem orqali 160+ belgili SMSlarni bo‘lib jo‘natish """
    try:
        # Serial portni ochish
        ser = serial.Serial(modem_port, baudrate=115200, timeout=5)
        time.sleep(2)

        # ✅ Modemni tayyorlash
        ser.write(b'AT\r')
        time.sleep(1)
        ser.write(b'AT+CMGF=1\r')  # Text rejimiga o'tish
        time.sleep(1)
        ser.write(b'AT+CSCS="GSM"\r')  # GSM matn rejimiga o'tish
        time.sleep(1)
        ser.write(b'AT+CSMP=17,167,0,0\r')  # SMS sozlamalarini to'g'ri qilish
        time.sleep(1)

        # ✅ SMSni 153 belgilik qismlarga bo‘lish
        parts = textwrap.wrap(message, 153)  # Har bir qism 153 belgi bo'ladi
        total_parts = len(parts)

        for i, part in enumerate(parts, start=1):
            print(f"📤 {i}/{total_parts} qism yuborilmoqda...")

            ser.write(f'AT+CMGS="{phone_number}"\r'.encode())
            time.sleep(1)
            ser.write(part.encode('utf-8') + b"\x1A")  # CTRL+Z tugmasi (SMS jo‘natish)
            time.sleep(8)  # ⏳ Uzoqroq kutish (8 soniya)

            # ✅ **GSM modem javobini kutish**
            response = ser.read(ser.inWaiting()).decode(errors='ignore')
            print(f"📥 GSM javobi: {response}")

            if "+CMS ERROR" in response:
                print(f"❌ {i}-qism yuborishda xatolik! ❌")
                ser.close()
                return False  # Agar SMS yuborishda muammo bo‘lsa, jarayon to‘xtaydi

        ser.close()
        print(f"✅ SMS {total_parts} qismda muvaffaqiyatli yuborildi!")
        return True

    except Exception as e:
        print(f"❌ SMS yuborishda xatolik: {e}")
        return False

if __name__ == "__main__":
    phone_number = input("Telefon raqamini kiriting (+998XXXXXXXXX): ").strip()
    message = input("SMS matnini kiriting: ").strip()

    if send_sms(phone_number, message):
        print("✅ SMS muvaffaqiyatli jo‘natildi!")
    else:
        print("❌ Xatolik yuz berdi, iltimos tekshiring!")

# 6 bo'lekke bo'lip jeberedi
# import serial
# import time
# import textwrap
# import binascii
#
# def send_sms(phone_number, message, modem_port="COM8"):
#     """ USB modem orqali 160+ belgili SMSlarni bo‘lib jo‘natish (Unicode UCS2) """
#     try:
#         # Serial portni ochish
#         ser = serial.Serial(modem_port, baudrate=115200, timeout=5)
#         time.sleep(2)
#
#         # ✅ Modemni Unicode UCS2 formatiga o'tkazish
#         ser.write(b'AT\r')
#         time.sleep(1)
#         ser.write(b'AT+CMGF=1\r')  # Text rejimiga o'tish
#         time.sleep(1)
#         ser.write(b'AT+CSCS="UCS2"\r')  # UCS2 Unicode rejimiga o'tish
#         time.sleep(1)
#         ser.write(b'AT+CSMP=17,167,0,8\r')  # SMS UCS2 formatida yuborish uchun sozlash
#         time.sleep(1)
#
#         # ✅ Telefon raqamini Unicode formatga o‘girish
#         phone_hex = binascii.hexlify(phone_number.encode('utf-16-be')).decode().upper()
#
#         # ✅ Matnni 70 belgidan iborat qismlarga bo‘lish (UCS2 uchun)
#         parts = textwrap.wrap(message, 70)
#         total_parts = len(parts)
#
#         for i, part in enumerate(parts, start=1):
#             # ✅ Matnni Unicode UCS2 formatga o‘girish
#             part_hex = binascii.hexlify(part.encode('utf-16-be')).decode().upper()
#
#             print(f"📤 {i}/{total_parts} qism yuborilmoqda...")
#
#             ser.write(f'AT+CMGS="{phone_hex}"\r'.encode())
#             time.sleep(1)
#             ser.write(part_hex.encode() + b"\x1A")  # CTRL+Z tugmasi (SMS jo‘natish)
#             time.sleep(8)  # ⏳ Uzoqroq kutish (8 soniya)
#
#             # ✅ **GSM modem javobini kutish**
#             response = ser.read(ser.inWaiting()).decode(errors='ignore')
#             print(f"📥 GSM javobi: {response}")
#
#             if "+CMS ERROR" in response:
#                 print(f"❌ {i}-qism yuborishda xatolik! ❌")
#                 ser.close()
#                 return False  # Agar SMS yuborishda muammo bo‘lsa, jarayon to‘xtaydi
#
#         ser.close()
#         print(f"✅ SMS {total_parts} qismda muvaffaqiyatli yuborildi!")
#         return True
#
#     except Exception as e:
#         print(f"❌ SMS yuborishda xatolik: {e}")
#         return False
#
# if __name__ == "__main__":
#     phone_number = input("Telefon raqamini kiriting (+998XXXXXXXXX): ").strip()
#     message = input("SMS matnini kiriting: ").strip()
#
#     if send_sms(phone_number, message):
#         print("✅ SMS muvaffaqiyatli jo‘natildi!")
#     else:
#         print("❌ Xatolik yuz berdi, iltimos tekshiring!")



















# import serial
# import time
# #COM8
# def send_sms(phone_number, message, modem_port="COM8"):
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

# import serial
# import time
# import textwrap
#
# def send_sms(phone_number, message, modem_port="COM12"):
#     """ USB modem orqali 160+ belgili SMSlarni bo‘lib jo‘natish """
#     try:
#         # Serial portni ochish
#         ser = serial.Serial(modem_port, baudrate=115200, timeout=5)
#         time.sleep(2)
#
#         # ✅ Modemni tayyorlash
#         ser.write(b'AT\r')
#         time.sleep(1)
#         ser.write(b'AT+CMGF=1\r')  # Text rejimiga o'tish
#         time.sleep(1)
#         ser.write(b'AT+CSCS="GSM"\r')  # GSM matn rejimiga o'tish
#         time.sleep(1)
#         ser.write(b'AT+CSMP=17,167,0,0\r')  # SMS sozlamalarini to'g'ri qilish
#         time.sleep(1)
#
#         # ✅ SMSni 153 belgilik qismlarga bo‘lish
#         parts = textwrap.wrap(message, 158)  # Har bir qism 153 belgi bo'ladi
#         total_parts = len(parts)
#
#         for i, part in enumerate(parts, start=1):
#             print(f"📤 {i}/{total_parts} qism yuborilmoqda...")
#
#             ser.write(f'AT+CMGS="{phone_number}"\r'.encode())
#             time.sleep(1)
#             ser.write(part.encode('utf-8') + b"\x1A")  # CTRL+Z tugmasi (SMS jo‘natish)
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

# Telefon oqimadi
# import serial
# import time
# import binascii
# import math
#
#
# def encode_pdu(phone_number, message):
#     """
#     UDH bilan SMS'ni bo‘laklarga bo‘lish va PDU formatga o‘girish.
#     """
#
#     # Telefon raqamini PDU formatga o‘zgartirish
#     phone_number = phone_number.replace("+", "").replace(" ", "")
#     if len(phone_number) % 2 != 0:
#         phone_number += "F"  # Agar toq bo‘lsa, oxiriga "F" qo‘shish
#
#     formatted_phone = "".join([phone_number[i + 1] + phone_number[i] for i in range(0, len(phone_number), 2)])
#
#     # ✅ Unicode (UCS2) formatga o‘girish
#     message_hex = binascii.hexlify(message.encode("utf-16be")).decode().upper()
#
#     # ✅ SMS'ni 67 Unicode belgilik qismlarga bo‘lish (max 140 bayt)
#     max_part_length = 67 * 4  # UCS2 formatda 67 belgi = 134 bayt = 268 hex
#     message_segments = [message_hex[i:i + max_part_length] for i in range(0, len(message_hex), max_part_length)]
#     total_parts = len(message_segments)
#
#     ref_number = "A1"  # UDH Reference Number (random yoki 00)
#
#     pdus = []
#     for part_index, part in enumerate(message_segments, start=1):
#         udh = f"050003{ref_number}{total_parts:02X}{part_index:02X}"  # UDH header
#
#         # PDU yaratish
#         pdu = (
#                 "00" +  # SMSC (o‘zgarishsiz)
#                 "51" +  # PDU-Type: SMS-SUBMIT + UDH
#                 "00" +  # Message Reference (Telefon belgilaydi)
#                 f"{len(phone_number):02X}" +  # Raqam uzunligi
#                 "91" + formatted_phone +  # Raqam (PDU formatida)
#                 "00" +  # PID (Protocol Identifier)
#                 "08" +  # Data Coding Scheme (UCS2 / Unicode)
#                 f"{len(udh) // 2:02X}" + udh +  # User Data Header
#                 part  # Matnni UCS2 formatida joylash
#         )
#         pdus.append(pdu)
#
#     return pdus
#
#
# def send_long_sms(phone_number, message, modem_port="COM12"):
#     """USB modem orqali Unicode SMS jo‘natish (Concatenated SMS)."""
#     try:
#         ser = serial.Serial(modem_port, baudrate=115200, timeout=5)
#         time.sleep(2)
#
#         # ✅ Modemni to'g'ri sozlash
#         ser.write(b'AT+CSMS=1\r')  # SMS xizmatini yoqish
#         time.sleep(1)
#         ser.write(b'AT+CMGF=0\r')  # PDU Mode
#         time.sleep(1)
#         ser.write(b'AT+CSMP=49,167,0,8\r')  # SMS kodlash formatini to‘g‘ri qilish
#         time.sleep(1)
#
#         # ✅ SMS'ni bo‘laklarga bo‘lib yuborish
#         pdus = encode_pdu(phone_number, message)
#
#         for pdu in pdus:
#             pdu_length = int(len(pdu) / 2) - 1  # PDU uzunligini hisoblash
#             ser.write(f'AT+CMGS={pdu_length}\r'.encode())
#             time.sleep(1)
#             ser.write(pdu.encode() + b"\x1A")  # CTRL+Z bilan jo‘natish
#             time.sleep(8)
#
#             # ✅ GSM modem javobini tekshirish
#             response = ser.read(ser.inWaiting()).decode(errors='ignore')
#             print(f"📥 GSM javobi: {response}")
#
#             if "+CMS ERROR" in response:
#                 print("❌ Xatolik yuz berdi! ❌")
#                 ser.close()
#                 return False
#
#         ser.close()
#         print("✅ SMS muvaffaqiyatli yuborildi!")
#         return True
#
#     except Exception as e:
#         print(f"❌ Xatolik: {e}")
#         return False
#
#
# if __name__ == "__main__":
#     phone_number = input("Telefon raqamini kiriting (+998XXXXXXXXX): ").strip()
#     message = input("SMS matnini kiriting: ").strip()
#
#     if send_long_sms(phone_number, message):
#         print("✅ SMS muvaffaqiyatli jo‘natildi!")
#     else:
#         print("❌ Xatolik yuz berdi, iltimos tekshiring!")
#Bul aniq isledi 6 bo'lingen smslerdi 1 sms qilip beredi

import time
from gsmmodem.modem import GsmModem

# 🔹 Kiritiladigan ma'lumotlar
PORT = input("Huawei modem portini kiriting (masalan, COM12 yoki /dev/ttyUSB0): ")
BAUDRATE = 115200
NUMBER = input("SMS yuboriladigan raqamni kiriting (masalan, +998901234567): ")
MESSAGE = input("Yuboriladigan xabar matnini kiriting: ")

# 🔹 Modemga ulanish
print(f"Modem {PORT} portida ishga tushirilmoqda...")
modem = GsmModem(PORT, BAUDRATE)
modem.connect()

# 🔹 Uzun SMSni jo'natish
print(f"{NUMBER} raqamiga SMS yuborilmoqda...")
response = modem.sendSms(NUMBER, MESSAGE)

if response:
    print("📩 SMS muvaffaqiyatli yuborildi!")
else:
    print("⚠️ SMS yuborishda xatolik yuz berdi!")

# 🔹 Modemni uzish
modem.close()

# from gsmmodem.modem import GsmModem, SentSms
#
# # 🔹 Kiritiladigan ma'lumotlar
# PORT = input("Huawei modem portini kiriting (masalan, COM12 yoki /dev/ttyUSB0): ")
# BAUDRATE = 115200
# NUMBER = input("SMS yuboriladigan raqamni kiriting (masalan, +998901234567): ")
# MESSAGE = input("Yuboriladigan xabar matnini kiriting: ")
#
# # 🔹 Modemga ulanish
# print(f"📡 Modem {PORT} portida ishga tushirilmoqda...")
# modem = GsmModem(PORT, BAUDRATE)
# modem.connect()
#
# # 🔹 **Eski SMS xabarlarini o‘chirish**
# print("🗑️ Modemdagi barcha SMS xabarlarini o‘chiramiz...")
#
# try:
#     messages = modem.listStoredSms()  # 📥 Barcha SMS xabarlarini olish
#     for msg in messages:
#         modem.deleteStoredSms(msg.memoryIndex)  # 🗑️ Har bir SMS'ni o‘chirish
#         print(f"🗑️ SMS o‘chirildi: {msg.number} - {msg.text[:30]}...")
# except Exception as e:
#     print(f"⚠️ Xabarlarni o‘chirishda xatolik yuz berdi: {str(e)}")
#
# # 🔹 **SMS jo‘natish**
# print(f"📩 {NUMBER} raqamiga SMS yuborilmoqda...")
# response = modem.sendSms(NUMBER, MESSAGE)
#
# if response:
#     print("✅ SMS muvaffaqiyatli yuborildi!")
# else:
#     print("⚠️ SMS yuborishda xatolik yuz berdi!")
#
# # 🔹 **Modemni uzish**
# modem.close()
# print("🔌 Modem uzildi.")


























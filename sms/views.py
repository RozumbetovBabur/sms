from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse
from .forms import *
import pandas as pd
import serial.tools.list_ports
import serial
from gsmmodem.modem import GsmModem
import re
import time
import textwrap
import binascii
from .models import *
import json
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.

@login_required(login_url="login")
def Home(request):
    return render(request,"base.html")

@login_required(login_url="login")
def create_sms(request):
    form = DebitorForm()
    form2 = CreateSMSForm()

    if request.method == "POST":
        form = DebitorForm(request.POST)
        form2 = CreateSMSForm(request.POST)

        if form.is_valid():
            form.save()
        if form2.is_valid():
            form2.save()
            return redirect('create_sms')

    context = {
        "form": form,
        "form2": form2,
    }

    return render(request, "create_sms.html", context)





@login_required(login_url="login")
def segin(request):
    error_massage = None
    if request.POST:
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            error_massage = "Terilgen parol birdey boliw kerek!"
        else:
            my_user = User.objects.create_user(username=username,first_name=first_name, email=email, password=password)
            my_user.first_name = first_name
            return redirect("login")
    return render(request,"signup.html", {"error_massage": error_massage})

def Login(request):
    error_message = None
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user is not None:
                login(request, user)
                return redirect("home")
        else:
            error_message = "Login yamasa paroldi qate kiritiniz, basqatdan urinip korin!!!"

    return render(request, "login.html", {"error_message": error_message})

@login_required(login_url="login")
def logout(request):
    auth_logout(request)
    return redirect("login")

@login_required(login_url="login")
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form, 'username': request.user.username})


@login_required(login_url="login")
def upload_excel(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        df = pd.read_excel(file, dtype=str)

        df.columns = df.columns.str.strip()

        required_columns = [
            "Ijro ish raqami",
            "Ijro hujjat raqami",
            "Ijro hujjat mazmuni",
            "Qoldiq summa",
            "Qarzdor F.I.SH",
            "Telefon raqami mavjudmi?",
            "Operator F.I.SH",
            "operator Telefon raqami mavjudmi?"
        ]
        for col in required_columns:
            if col not in df.columns:
                messages.error(request, f"Xatolik: '{col}' ustuni Excel faylida topilmadi!")
                return redirect("upload_excel")
                # return HttpResponse(f"Xatolik: '{col}' Excel faylidan tabilmadi!", status=400)

        def clean_number(value):
            if isinstance(value, str):
                value = value.replace(" ", "").replace(",", ".")
            try:
                return round(float(value), 2)
            except ValueError:
                return None

        df["Qoldiq summa"] = df["Qoldiq summa"].apply(clean_number)

        # Bazaga saqlash
        for _, row in df.iterrows():
            DebitorSms.objects.create(
                ijro_ish_raqami=row["Ijro ish raqami"],
                ijro_hujjat_raqami=row["Ijro hujjat raqami"],
                ijro_hujjat_mazmuni=row["Ijro hujjat mazmuni"],
                ijro_hujjat_summasi=row["Qoldiq summa"],
                qarzdor_fish=row["Qarzdor F.I.SH"],
                telefon_raqami=row["Telefon raqami mavjudmi?"],
                operator_fish=row["Operator F.I.SH"],
                operator_telefon_raqami=row["operator Telefon raqami mavjudmi?"]
            )

        messages.success(request, "✅ Excel mag'luwmatlar toliq juklendi!")
        return redirect("upload_excel")
        # return HttpResponse("Excel Mag'luwmatlar toliq juklendi!")

    return render(request, "upload_excel.html")

def debitor_list(request):
    debitors = DebitorSms.objects.all()
    return render(request, "debitor_list.html", {"debitors": debitors})

def format_phone_number(phone_number):
    """Telefon raqamni +998XXXXXXXXX formatiga o‘tkazish"""
    phone_number = re.sub(r'\D', '', phone_number)  # ❌ Raqam bo‘lmagan belgilarni olib tashlash

    if phone_number.startswith("998"):
        phone_number = f"+{phone_number}"  # ✅ Agar oldida 998 bo‘lsa, faqat + qo‘shiladi
    elif len(phone_number) == 9:
        phone_number = f"+998{phone_number}"  # ✅ Agar faqat 9 xonali raqam bo‘lsa, +998 qo‘shiladi

    return phone_number

def generate_sms_view(request):
    if request.method == "POST":
        debitors = DebitorSms.objects.all()

        for debitor in debitors:
            # 🔹 Telefon raqamni formatlash
            formatted_phone = format_phone_number(debitor.telefon_raqami)

            # 🔹 Agar ushbu debitor uchun oldin SMS generatsiya qilingan bo'lsa, o'tkazib yuboramiz
            if DebitorSendGetSMS.objects.filter(debitor_sms=debitor).exists():
                continue

            # 🔹 SMS matni generatsiyasi
            sms_text = f"Prokuratura Byurosi tomonidan {debitor.qarzdor_fish} Sizga nisbatan {debitor.ijro_hujjat_summasi} so'mlik {debitor.ijro_hujjat_raqami} sonli ijro ishi mavjud. Jami {debitor.ijro_hujjat_summasi} so'm to'lanmagan taqdirda, mol-mulkingizga taqiq solinib, avtotransportingizga qidiruv e’lon qilinadi. Agarda qarzdorlik o’z vaqtida qoplanmagan taqdirda BXM ning 5 baravarigacha jarima qollanilishi haqida ogohlantiramiz. To'lov uchun ID: {debitor.ijro_ish_raqami} Davlat ijrochisi: {debitor.operator_fish} Tel: {debitor.operator_telefon_raqami}, +998939202082"

            # 🔹 Yangi SMS generatsiya qilib bazaga saqlaymiz
            DebitorSendGetSMS.objects.create(debitor_sms=debitor, telefon_raqami=formatted_phone, sms_text=sms_text)

        return redirect("generate-list")

    return render(request, "generate_sms.html")


# def generate_sms_view(request):
#     if request.method == "POST":
#         debitors = DebitorSms.objects.all()
#         for debitor in debitors:
#             # sms_text = f"Ҳурматли {debitor.qarzdor_fish}, Сизнинг {debitor.ijro_ish_raqami} суд иши бўйича {debitor.ijro_hujjat_raqami}. Сизда {debitor.ijro_hujjat_mazmuni} {debitor.ijro_hujjat_summasi} сўм қарздорлик мавжуд. Тўлов учун ИД: {debitor.ijro_ish_raqami}. Ижрочи {debitor.operator_fish}, Тел: {debitor.operator_telefon_raqami} mib.uz"
#             sms_text = f"Prokuratura Byurosi tomonidan {debitor.qarzdor_fish} Sizga nisbatan {debitor.ijro_hujjat_summasi} so'mlik {debitor.ijro_hujjat_raqami} sonli ijro ishi mavjud. Jami {debitor.ijro_hujjat_summasi} so'm to'lanmagan taqdirda, mol-mulkingizga taqiq solinib, avtotransportingizga qidiruv e’lon qilinadi. Agarda qarzdorlik o’z vaqtida qoplanmagan taqdirda BXM ning 5 baravarigacha jarima qollanilishi haqida ogohlantiramiz. To'lov uchun ID: {debitor.ijro_ish_raqami} Davlat ijrochisi: {debitor.operator_fish} Tel: {debitor.operator_telefon_raqami}"
#             # sms_text = f"{debitor.qarzdor_fish} {debitor.ijro_hujjat_summasi} {debitor.ijro_hujjat_raqami} {debitor.ijro_hujjat_summasi} {debitor.ijro_ish_raqami}, {debitor.operator_fish} {debitor.operator_telefon_raqami}"
#
#             # DebitorSend bazag'a saqlaw
#             DebitorSendGet.objects.create(debitor_sms=debitor, sms_text=sms_text)
#
#         return redirect("generate-list")
#
#     return render(request, "generate_sms.html")

def sms_list_view(request):
    sms_list = DebitorSendGetSMS.objects.all().order_by("-created_at")
    return render(request, "sms_list.html", {"sms_list": sms_list})



def debitor_list_view(request):
    debitors = DebitorSend.objects.all().order_by('-id')  # So'nggi qo‘shilganlar birinchi chiqadi
    return render(request, 'generate_list.html', {'debitors': debitors})

# Start USB modem
def get_modem_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "ZTE Proprietary" in port.description:  # Huawei modemni topish
            return port.device
    return "COM18"

# def format_phone_number(phone_number):
#     # ✅ 1️⃣ Bo‘sh joylar, chiziqlar va nuqtalarni olib tashlash
#     phone_number = re.sub(r"[^\d]", "", phone_number)
#
#     # ✅ 2️⃣ Agar uzunligi 9 bo‘lsa (masalan, "937156633"), +998 qo‘shish
#     if len(phone_number) == 9 and phone_number.startswith("9"):
#         phone_number = f"+998{phone_number}"
#
#     # ✅ 3️⃣ Agar allaqachon +998 bilan boshlangan bo‘lsa, o‘zgartirmaslik
#     elif len(phone_number) == 12 and phone_number.startswith("998"):
#         phone_number = f"+{phone_number}"
#
#     return phone_number


def modem_port_view(request):
    port = get_modem_port()
    return render(request, "modem_port.html", {"port": port})

BAUDRATE = 115200  # Modemning ishlash tezligi
RETRY_INTERVAL = 10  # Port band bo'lsa, qayta urinish vaqti (soniya)
WAIT_TIME = 50  # Har bir SMS yuborilgandan keyin kutish vaqti (5 daqiqa)
MAX_SMS_COUNT = 15  # 🔹 Bir martada jo‘natiladigan maksimal SMS soni
INVALID_SMS_STORAGE = []  # 🔹 Xato raqamli SMS-larni saqlash
FAILED_SMS_STORAGE = []  # ❌ Yuborishda xato bo‘lgan SMSlar uchun
MODEM_WAIT_TIME = 10  # ✅ Modem tayyorligini tekshirish vaqti (sekund)

def is_valid_phone_number(phone_number):
    """Telefon raqam to'g'ri ekanligini tekshiradi (+998 bilan boshlanishi va 9 ta raqam bo‘lishi kerak)"""
    return bool(re.fullmatch(r"^\+998\d{9}$", phone_number))


def is_modem_ready(modem):
    """Modemning keyingi SMS yuborishga tayyorligini tekshirish"""
    while True:
        try:
            signal_strength = modem.signalStrength
            print(f"📶 Modem signal kuchi: {signal_strength}")
            if signal_strength > 5:  # ✅ Signal kuchi yetarli bo'lsa, davom etamiz
                return True
        except Exception as e:
            print(f"⚠️ Modem hali tayyor emas, kutamiz... ({str(e)})")

        time.sleep(MODEM_WAIT_TIME)  # ✅ Modem tayyor bo‘lishini kutamiz

def send_sms_via_modem(phone_number, message):
    """SMS modem orqali jo‘natish va port band bo‘lsa, qayta urinish"""
    while True:
        try:
            modem_port = get_modem_port()
            if not modem_port:
                print("⚠️ Modem topilmadi, 10 soniya kutamiz...")
                time.sleep(RETRY_INTERVAL)
                continue



            print(f"📡 Modem {modem_port} portida ishga tushirilmoqda...")

            modem = GsmModem(modem_port, BAUDRATE)
            modem.connect()

            if is_modem_ready(modem):  # ✅ Modem tayyor bo‘lguncha kutamiz
                print(f"📩 {phone_number} raqamiga SMS yuborilmoqda...")
                response = modem.sendSms(phone_number, message)
                modem.close()  # Modemni uzish

            # print(f"📩 {phone_number} raqamiga SMS yuborilmoqda...")
            #
            # response = modem.sendSms(phone_number, message)
            # modem.close()  # Modemni uzish

                if response:
                    print("✅ SMS muvaffaqiyatli yuborildi!")
                    return True
                else:
                    print("❌ SMS yuborishda xatolik yuz berdi!")
                    return False
            else:
                print("⚠️ Modem hali tayyor emas, yana kutamiz...")
                time.sleep(MODEM_WAIT_TIME)

        except serial.SerialException:
            print("⚠️ Port band! 10 soniya kutamiz...")
            time.sleep(RETRY_INTERVAL)
        except Exception as e:
            print(f"⚠️ Xatolik yuz berdi: {str(e)}")
            return False

# Progressni saqlash uchun global o'zgaruvchi
PROGRESS_DATA = {"sent": 0, "total": 0, "completed": False, "sent_sms": [], "failed_sms": [], "invalid_sms": []}

#Button skritiy boldi ishlap turipdi
# @login_required(login_url="login")
# def send_sms_from_debitors(request):
#     """SMS jo‘natish va progressni qaytarish"""
#     global PROGRESS_DATA, INVALID_SMS_STORAGE, FAILED_SMS_STORAGE
#
#     if request.method == "POST":
#         sms_entries = DebitorSendGetSMS.objects.all()[:MAX_SMS_COUNT]
#         total_sms = sms_entries.count()
#
#         if total_sms == 0:
#             return render(request, "send_sms.html", {"error": "⚠️ Jo‘natish uchun hech qanday SMS topilmadi."})
#
#         # Progressni boshlash
#         PROGRESS_DATA = {"sent": 0, "total": total_sms, "completed": False, "sent_sms": [], "failed_sms": []}
#         INVALID_SMS_STORAGE = []  # Xato raqamlar uchun ro‘yxatni tozalash
#         FAILED_SMS_STORAGE = []  # ❌ Jo‘natishda xato bo‘lgan SMSlar uchun
#
#         for sms_entry in sms_entries:
#             phone_number = sms_entry.telefon_raqami.strip()
#             sms_text = sms_entry.sms_text.strip()
#             debitor_sms = sms_entry.debitor_sms
#
#             if not is_valid_phone_number(phone_number):
#                 # Xato formatdagi raqamni INVALID_SMS_STORAGE ga saqlash
#                 INVALID_SMS_STORAGE.append({"phone_number": phone_number, "sms_text": sms_text, "status": "Noto‘g‘ri format"})
#                 continue  # Keyingi raqamga o‘tish
#
#             if send_sms_via_modem(phone_number, sms_text):
#                 debitor_sms.delete()
#                 PROGRESS_DATA["sent_sms"].append({"phone_number": phone_number, "sms_text": sms_text, "status": "Yuborildi"})
#             else:
#                 FAILED_SMS_STORAGE.append({"phone_number": phone_number, "sms_text": sms_text, "status": "Xatolik"})
#                 PROGRESS_DATA["failed_sms"].append({"phone_number": phone_number, "sms_text": sms_text, "status": "Xatolik"})
#
#             PROGRESS_DATA["sent"] += 1  # SMS jo‘natildi
#             time.sleep(1)  # 1 soniya kutish
#
#         PROGRESS_DATA["completed"] = True  # Barcha SMS jo‘natildi
#         return render(request, "sms_send.html", {
#             "sent_sms": PROGRESS_DATA["sent_sms"],
#             "failed_sms": PROGRESS_DATA["failed_sms"],
#             "invalid_sms": INVALID_SMS_STORAGE,
#             "progress": int((PROGRESS_DATA["sent"] / total_sms) * 100)
#         })
#
#     return render(request, "sms_send.html")
#Button skritiy boldi ishlap turipdi

@login_required(login_url="login")
def send_sms_from_debitors(request):
    """SMS jo‘natish va progressni qaytarish"""
    global PROGRESS_DATA, INVALID_SMS_STORAGE, FAILED_SMS_STORAGE

    if request.method == "POST":
        sms_entries = DebitorSendGetSMS.objects.all()[:MAX_SMS_COUNT]
        total_sms = sms_entries.count()

        if total_sms == 0:
            return JsonResponse({"success": False, "error": "⚠️ Jo‘natish uchun hech qanday SMS topilmadi."})

        # Progressni boshlash
        PROGRESS_DATA = {"sent": 0, "total": total_sms, "completed": False, "sent_sms": [], "failed_sms": [], "invalid_sms": []}
        INVALID_SMS_STORAGE = []
        FAILED_SMS_STORAGE = []

        for sms_entry in sms_entries:
            phone_number = sms_entry.telefon_raqami.strip()
            sms_text = sms_entry.sms_text.strip()
            debitor_sms = sms_entry.debitor_sms

            if not is_valid_phone_number(phone_number):
                INVALID_SMS_STORAGE.append({"phone_number": phone_number, "sms_text": sms_text, "status": "Noto‘g‘ri format"})
                PROGRESS_DATA["invalid_sms"].append({"phone_number": phone_number, "sms_text": sms_text, "status": "Noto‘g‘ri format"})
                continue

            if send_sms_via_modem(phone_number, sms_text):
                debitor_sms.delete()
                PROGRESS_DATA["sent_sms"].append({"phone_number": phone_number, "sms_text": sms_text, "status": "Yuborildi"})
            else:
                FAILED_SMS_STORAGE.append({"phone_number": phone_number, "sms_text": sms_text, "status": "Xatolik"})
                PROGRESS_DATA["failed_sms"].append({"phone_number": phone_number, "sms_text": sms_text, "status": "Xatolik"})

            PROGRESS_DATA["sent"] += 1
            # time.sleep(WAIT_TIME)

            print(f"⏳ SMS jo‘natildi, modem dam olishi uchun {MODEM_WAIT_TIME} soniya kutamiz...")
            time.sleep(MODEM_WAIT_TIME)  # ✅ Modem haddan tashqari yuklanmasligi uchun kutamiz

        PROGRESS_DATA["completed"] = True

        return JsonResponse({"success": True})

    # Agar GET so‘rovi bo‘lsa, sahifani qaytaramiz
    return render(request, "sms_send.html")

def get_sms_progress(request):
    """SMS jo‘natish progressini qaytarish"""
    global PROGRESS_DATA
    print("🟢 PROGRESS_DATA:", json.dumps(PROGRESS_DATA, indent=4))

    return JsonResponse({
        "sent": PROGRESS_DATA["sent"],
        "total": PROGRESS_DATA["total"],
        "completed": PROGRESS_DATA["completed"],
        "successful_sms": len(PROGRESS_DATA["sent_sms"]),
        "failed_sms_count": len(PROGRESS_DATA["failed_sms"]),
        "failed_sms": PROGRESS_DATA["failed_sms"],
        "sent_sms": PROGRESS_DATA["sent_sms"],
        "invalid_sms": PROGRESS_DATA["invalid_sms"]
    })



# @login_required(login_url="login")
# def send_sms_from_debitors(request):
#     """Bazadagi SMS-larni modem orqali jo‘natadi (20 tadan ko‘p emas)"""
#     if request.method == "POST":
#         sms_entries = DebitorSendGetSMS.objects.all()[:MAX_SMS_COUNT]
#
#         if not sms_entries.exists():
#             messages.warning(request, "⚠️ Jo‘natish uchun hech qanday SMS topilmadi.")
#             return redirect("send_sms_from_debitors")
#
#         sent_sms_list = []  # Yuborilgan SMSlar ro‘yxati
#         failed_sms_list = []  # Noto‘g‘ri yoki yuborilmagan SMSlar ro‘yxati
#
#         for sms_entry in sms_entries:
#             phone_number = sms_entry.telefon_raqami.strip()
#             sms_text = sms_entry.sms_text.strip()
#             debitor_sms = sms_entry.debitor_sms
#
#             if not is_valid_phone_number(phone_number):
#                 failed_sms_list.append({"phone_number": phone_number, "sms_text": sms_text, "status": "Noto‘g‘ri raqam"})
#                 messages.error(request, f"❌ Noto‘g‘ri telefon raqam: {phone_number}")
#                 continue
#
#             if send_sms_via_modem(phone_number, sms_text):
#                 messages.success(request, f"✅ SMS jo‘natildi: {phone_number}")
#                 sent_sms_list.append({"phone_number": phone_number, "sms_text": sms_text, "status": "Yuborildi"})
#                 debitor_sms.delete()
#                 print("⌛ 10 soniya kutamiz...")
#                 time.sleep(WAIT_TIME)
#
#             else:
#                 messages.error(request, f"❌ SMS jo‘natishda xatolik: {phone_number}")
#                 failed_sms_list.append({"phone_number": phone_number, "sms_text": sms_text, "status": "Xatolik"})
#
#         # Malumotlarni session orqali uzatish
#         request.session["sent_sms_list"] = sent_sms_list
#         request.session["failed_sms_list"] = failed_sms_list
#
#         return redirect("send_sms_from_debitors")
#
#     # Sahifaga yuborilgan va yuborilmagan SMSlar ro‘yxatini uzatish
#     sent_sms_list = request.session.pop("sent_sms_list", [])
#     failed_sms_list = request.session.pop("failed_sms_list", [])
#     sms_list = DebitorSendGetSMS.objects.all()
#
#     return render(request, "sms_send.html", {
#         "sms_list": sms_list,
#         "sent_sms_list": sent_sms_list,
#         "failed_sms_list": failed_sms_list
#     })

# @login_required(login_url="login")
# def send_sms_from_debitors(request):
#     """Bazadagi SMS-larni modem orqali jo‘natadi (20 tadan ko‘p emas)"""
#     if request.method == "POST":
#         sms_entries = DebitorSendGetSMS.objects.all()[:MAX_SMS_COUNT]  # 🔹 20 ta SMS tanlash
#
#         if not sms_entries.exists():
#             messages.warning(request, "⚠️ Jo‘natish uchun hech qanday SMS topilmadi.")
#             return redirect("send_sms_from_debitors")
#
#         sent_sms_count = 0
#         failed_sms_count = 0
#
#         for sms_entry in sms_entries:
#             phone_number = sms_entry.telefon_raqami.strip()  # Telefon raqam to‘g‘ridan-to‘g‘ri bazadan olinadi
#             sms_text = sms_entry.sms_text.strip()
#             debitor_sms = sms_entry.debitor_sms  # Ushbu SMS ga tegishli DebitorSms yozuvi
#
#             if not is_valid_phone_number(phone_number):
#                 INVALID_SMS_STORAGE.append({"Telefon raqam": phone_number, "text": sms_text})
#                 messages.error(request, f"❌ Noto‘g‘ri telefon raqam: {phone_number}")
#                 failed_sms_count += 1
#                 continue  # Keyingi SMSga o‘tish
#
#             if send_sms_via_modem(phone_number, sms_text):
#                 messages.success(request, f"✅ SMS jo‘natildi: {phone_number}")
#                 sent_sms_count += 1
#                 debitor_sms.delete()  # SMS muvaffaqiyatli yuborilsa, bazadan o‘chiriladi
#                 print("⌛ 10 soniya kutamiz...")
#                 time.sleep(WAIT_TIME)  # 10 soniya kutish
#
#             else:
#                 messages.error(request, f"❌ SMS jo‘natishda xatolik: {phone_number}")
#
#         if sent_sms_count > 0:
#             messages.success(request, f"✅ Jami {sent_sms_count} ta SMS muvaffaqiyatli jo‘natildi va bazadan o‘chirildi!")
#             messages.error(request, f"❌ {failed_sms_count} ta SMS jo‘natilmadi!")
#
#         return redirect("send_sms_from_debitors")
#
#     sms_list = DebitorSendGetSMS.objects.all()
#     return render(request, "sms_send.html", {"sms_list": sms_list})

def clear_modem_sms(request):
    """Modemdagi barcha SMS xabarlarini o‘chiradi."""
    try:
        modem_port = get_modem_port()
        modem = GsmModem(modem_port, BAUDRATE)
        modem.connect()
        messages_list = modem.listStoredSms()  # 📥 Barcha SMS'larni olish

        if not messages_list:
            messages.info(request, "✅ Modemda SMS xabarlar yo‘q!")
        else:
            for msg in messages_list:
                modem.deleteStoredSms(msg.memoryIndex)  # 🗑️ SMS'ni o‘chirish
            messages.success(request, f"🗑️ {len(messages_list)} ta SMS modemdan o‘chirildi!")

        modem.close()
    except Exception as e:
        messages.error(request, f"⚠️ Xatolik: {str(e)}")

    return render(request, "sms_dashboard.html")  # ✅ Sahifani qaytarish


# End USB modem




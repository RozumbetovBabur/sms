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
import time
import textwrap
import binascii
from .models import *
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


def generate_sms_view(request):
    if request.method == "POST":
        debitors = DebitorSms.objects.all()
        for debitor in debitors:
            # sms_text = f"Ҳурматли {debitor.qarzdor_fish}, Сизнинг {debitor.ijro_ish_raqami} суд иши бўйича {debitor.ijro_hujjat_raqami}. Сизда {debitor.ijro_hujjat_mazmuni} {debitor.ijro_hujjat_summasi} сўм қарздорлик мавжуд. Тўлов учун ИД: {debitor.ijro_ish_raqami}. Ижрочи {debitor.operator_fish}, Тел: {debitor.operator_telefon_raqami} mib.uz"
            sms_text = f"Prokuratura Byurosi tomonidan {debitor.qarzdor_fish} Sizga nisbatan {debitor.ijro_hujjat_summasi} so'mlik {debitor.ijro_hujjat_raqami} sonli ijro ishi mavjud. Jami {debitor.ijro_hujjat_summasi} so'm to'lanmagan taqdirda, mol-mulkingizga taqiq solinib, avtotransportingizga qidiruv e’lon qilinadi, majburiy ijro etish choralari qo’llaniladi. To'lov uchun ID: {debitor.ijro_ish_raqami}, ijrochi {debitor.operator_fish} Tel: {debitor.operator_telefon_raqami}"
            # sms_text = f"{debitor.qarzdor_fish} {debitor.ijro_hujjat_summasi} {debitor.ijro_hujjat_raqami} {debitor.ijro_hujjat_summasi} {debitor.ijro_ish_raqami}, {debitor.operator_fish} {debitor.operator_telefon_raqami}"

            # DebitorSend bazag'a saqlaw
            DebitorSendGet.objects.create(debitor_sms=debitor, sms_text=sms_text)

        return redirect("generate-list")

    return render(request, "generate_sms.html")

def sms_list_view(request):
    sms_list = DebitorSendGet.objects.all().order_by("-created_at")
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
    return "COM7"

# def get_modem_port():
#     import serial.tools.list_ports
#     ports = serial.tools.list_ports.comports()
#     for port in ports:
#         if "Huawei" in port.description or "ZTE Proprietary" in port.description:
#             print(f"✅ Modem tabilmadi: {port.device}")
#             return port.device
#     print("⚠️ Modem tabilmadi, COM8 portan paydalanmaqta!")
#     return "COM8"


# def format_phone_number(phone_number):
#     phone_number = phone_number.strip()
#     if not phone_number.startswith("+"):
#         phone_number = f"+{phone_number}"
#     return phone_number

def format_phone_number(phone_number):
    phone_number = phone_number.strip()
    if not phone_number.startswith("+"):
        phone_number = f"+{phone_number}"
    return phone_number


def modem_port_view(request):
    port = get_modem_port()
    return render(request, "modem_port.html", {"port": port})



def send_sms_via_modem(phone_number, message):
    modem_port = get_modem_port()

    phone_number = format_phone_number(phone_number)

    try:
        ser = serial.Serial(modem_port, baudrate=115200, timeout=5)
        time.sleep(1)

        # AT komandalardi jeberiw ha'm na'tejeni tekseriw
        ser.write(b'AT\r')
        time.sleep(1)
        response = ser.read(64).decode(errors='ignore')
        if "OK" not in response:
            print("❌ Modemden juwap kelmedi!")
            ser.close()
            return False

        ser.write(b'AT+CMGF=1\r')  # Text rejimge o'tiw
        time.sleep(1)
        ser.write(f'AT+CMGS="{phone_number}"\r'.encode())
        time.sleep(1)
        ser.write(message.encode() + b"\x1A")
        time.sleep(3)

        response = ser.read(64).decode(errors='ignore')
        ser.close()

        if "OK" in response:
            print(f"✅ SMS jeberildi: {phone_number}")
            return True  # SMS jeberildi
        else:
            print(f"❌ SMS jo‘natishda xatolik: {response}")
            return False
    except Exception as e:
        print(f"❌ Qa'te juzberdi: {e}")
        return False


# def send_sms_via_modem(phone_number, message):
#
#     """ USB Modem orqali SMS jo‘natish funksiyasi """
#     modem_port = get_modem_port()
#     if modem_port is None:
#         print("❌ USB modem topilmadi! SMS jo‘natilmadi.")
#         return False
#
#     phone_number = format_phone_number(phone_number)  # Telefon raqamini formatlash
#
#     try:
#         ser = serial.Serial(modem_port, baudrate=115200, timeout=5)
#         time.sleep(1)
#
#         # AT komandalar yuborish
#         ser.write(b'AT\r')
#         time.sleep(1)
#         ser.write(b'AT+CMGF=1\r')
#         time.sleep(1)
#         ser.write(f'AT+CMGS="{phone_number}"\r'.encode())
#         time.sleep(1)
#         ser.write(message.encode() + b"\x1A")
#         time.sleep(3)
#
#         ser.close()
#         print(f"✅ SMS jeberildi! {phone_number}")
#         return True
#     except Exception as e:
#         print(f"❌ SMS jeberiwde qatelik: {e}")
#         return False




@login_required(login_url="login")
def send_sms_from_debitors(request):
    if request.method == "POST":
        debitors = DebitorSms.objects.exclude(telefon_raqami=None).exclude(telefon_raqami="")

        if not debitors.exists():
            messages.warning(request, "⚠️ Jeberiw ushin nesh qanday sms tabilmadi.")
            return redirect("send_sms_from_debitors")

        for debitor in debitors:
            sms_text_obj = DebitorSendGet.objects.filter(debitor_sms=debitor).first()
            if sms_text_obj and debitor.telefon_raqami:
                phone_number = format_phone_number(debitor.telefon_raqami)
                sms_text = sms_text_obj.sms_text.strip()

                if send_sms_via_modem(phone_number, sms_text):
                    messages.success(request, f"✅ SMS jeberildi: {phone_number}")
                else:
                    messages.error(request, f"❌ SMS jebergende qatelik boldi: {phone_number}")

        return redirect("send_sms_from_debitors")

    sms_list = DebitorSms.objects.all()
    return render(request, "sms_send.html", {"sms_list": sms_list})


#1


# @login_required(login_url="login")
# def send_sms(request):
#     """ SMS'larni jeberiw """
#     if request.method == "POST":
#         sms_ids = request.POST.getlist("sms_ids")
#         sms_list = CreateSMS.objects.filter(id__in=sms_ids, status=False)
#
#         for sms in sms_list:
#             if send_sms_via_modem(sms.debitor.phone, sms.mazmuni):
#                 sms.status = True
#                 sms.save()
#
#         return redirect("sms_list")
#
#     sms_list = CreateSMS.objects.all()
#     return render(request, "sms_list.html", {"sms_list": sms_list})
#
# @login_required(login_url="login")
# def sms_list(request):
#     sms_list = CreateSMS.objects.all()
#     return render(request, "sms_view.html", {"sms_list": sms_list})

# End USB modem


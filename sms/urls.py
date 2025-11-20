from django.urls import path
from .views import *

urlpatterns = [
    path('',Login,name="login"),
    path('home/',Home,name="home"),
    path('create/',create_sms,name="create_sms"),

    path('signup/',segin,name="segin"),
    path('logout/',logout,name="logout"),

    path('profile/', profile, name='profile'),

    path("upload/", upload_excel, name="upload_excel"),
    path('debitors/', debitor_list, name="debitor_list"),
    path("generate-sms/", generate_sms_view, name="generate_sms"),
    path("generate/list/",sms_list_view,name="generate-list"),
    path('debitors/', debitor_list_view, name="debitor_list"),
    path('send_sms_from_debitors/', send_sms_from_debitors, name='send_sms_from_debitors'),
    path("get_sms_progress/", get_sms_progress, name="get_sms_progress"),  # ✅ Yangi URL
    path("clear-modem-sms/", clear_modem_sms, name="clear_modem_sms"),

    path('modem-port/', modem_port_view, name="modem_port"),
    # path('send-sms/', send_sms, name="send_sms"),
    # path('sms-list/', sms_list, name="sms_list"),
]
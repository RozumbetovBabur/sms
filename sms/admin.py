from django.contrib import admin
from .models import *

# @admin.register(Debitor)
# class DebitorAdmin(admin.ModelAdmin):
#     list_display = ['id', 'fio', 'phone', 'qarz', 'passport', 'created_at']
#
# @admin.register(CreateSMS)
# class CreateSMSAdmin(admin.ModelAdmin):
#     list_display = ['id', 'debitor', 'ijro_raqami', 'mazmuni', 'selected', 'status', 'created_at']
#     list_filter = ['status', 'selected']
#     search_fields = ['debitor__fio', 'ijro_raqami', 'mazmuni']


admin.site.register(Debitor)
admin.site.register(CreateSMS)


admin.site.register(DebitorSms)

admin.site.register(DebitorSendGet)

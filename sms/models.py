from django.db import models

class Debitor(models.Model):
    fio = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    qarz = models.DecimalField(max_digits=10, decimal_places=2)
    passport = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fio

class CreateSMS(models.Model):
    debitor = models.ForeignKey(Debitor, on_delete=models.CASCADE)  # Debitor bilan bog‘lanish
    selected = models.BooleanField(default=False)
    ijro_raqami = models.CharField(max_length=14)  # String sifatida saqlash yaxshi
    mazmuni = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"SMS to {self.debitor.phone} - {'Sent' if self.status else 'Pending'}"

    def __str__(self):
        return f"{self.debitor.fio} - {self.mazmuni[:20]}"


class DebitorSms(models.Model):
    ijro_ish_raqami = models.CharField(max_length=50)
    ijro_hujjat_raqami = models.CharField(max_length=50)
    ijro_hujjat_mazmuni = models.TextField()
    ijro_hujjat_summasi = models.DecimalField(max_digits=15, decimal_places=2)
    qarzdor_fish = models.CharField(max_length=255)
    telefon_raqami = models.CharField(max_length=20, blank=True, null=True)
    operator_fish = models.CharField(max_length=255, blank=True, null=True)
    operator_telefon_raqami = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.qarzdor_fish}"


class DebitorSend(models.Model):
    ijro_ish_raqami = models.CharField(max_length=255, unique=True, verbose_name="Ijro Ish Raqami")
    ijro_hujjat_raqami = models.CharField(max_length=255, verbose_name="Ijro Hujjat Raqami")
    ijro_hujjat_mazmuni = models.CharField(max_length=500, verbose_name="Ijro Hujjat Mazmuni")
    ijro_hujjat_summasi = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Ijro Hujjati Summasi")
    qarzdor_fish = models.CharField(max_length=255, verbose_name="Qarzdor F.I.SH")
    telefon_raqami = models.CharField(max_length=20, verbose_name="Telefon Raqami")
    operator_fish = models.CharField(max_length=255, verbose_name="Operator F.I.SH")
    operator_telefon_raqami = models.CharField(max_length=20, verbose_name="Operator Telefon Raqami")

    sms_text = models.TextField(blank=True, null=True, verbose_name="Yaratilgan SMS Matni")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan Vaqt")

    def __str__(self):
        return f"{self.qarzdor_fish} - {self.ijro_ish_raqami}"



class DebitorUsi(models.Model):
    qarzdor_fish = models.CharField(max_length=255)
    ijro_hujjat_raqami = models.CharField(max_length=255)
    ijro_hujjat_mazmuni = models.TextField()
    ijro_hujjati_summasi = models.DecimalField(max_digits=12, decimal_places=2)
    ijro_ish_raqami = models.CharField(max_length=255)
    operator_fish = models.CharField(max_length=255)
    operator_telefon_raqami = models.CharField(max_length=20)

class DebitorSendUsi(models.Model):
    debitor = models.ForeignKey(Debitor, on_delete=models.CASCADE)
    sms_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class DebitorSendGet(models.Model):
    debitor_sms = models.ForeignKey(DebitorSms, on_delete=models.CASCADE)
    sms_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

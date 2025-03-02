# Generated by Django 4.2.19 on 2025-02-23 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0003_debitorsend'),
    ]

    operations = [
        migrations.CreateModel(
            name='DebitorUsi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qarzdor_fish', models.CharField(max_length=255)),
                ('ijro_hujjat_raqami', models.CharField(max_length=255)),
                ('ijro_hujjat_mazmuni', models.TextField()),
                ('ijro_hujjati_summasi', models.DecimalField(decimal_places=2, max_digits=12)),
                ('ijro_ish_raqami', models.CharField(max_length=255)),
                ('operator_fish', models.CharField(max_length=255)),
                ('operator_telefon_raqami', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DebitorSendUsi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('debitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.debitor')),
            ],
        ),
    ]

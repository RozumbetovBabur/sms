from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class DebitorForm(forms.ModelForm):
    class Meta:
        model = Debitor
        fields = ('fio', 'phone', 'qarz', 'passport')
        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'qarz': forms.NumberInput(attrs={'class': 'form-control'}),
            'passport': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileForm(UserChangeForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
        help_text="Оставьте поле пустым, если вы не хотите менять пароль."
    )

    class Meta:
        model = User
        fields = ['username','first_name', 'email', 'password']  # Include other fields as needed
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'first_name': forms.TextInput(attrs={"class" : "form-control"}),
            'email': forms.TextInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Update the password only if a new one is entered
        if commit:
            user.save()
        return user

class ExcelUploadForm(forms.Form):
    file = forms.FileField()


class CreateSMSForm(forms.ModelForm):
    class Meta:
        model = CreateSMS
        fields = ('debitor', 'ijro_raqami', 'mazmuni', 'selected')
        widgets = {
            'debitor': forms.Select(attrs={'class': 'form-control'}),  # Dropdown
            'ijro_raqami': forms.TextInput(attrs={'class': 'form-control'}),
            'mazmuni': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'selected': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

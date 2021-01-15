from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from .models import Contact

class ContactForm(forms.ModelForm):

    captcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ("email", "captcha")
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите ваш E-mail"})

        }
        labels = {
            "email": ''
        }
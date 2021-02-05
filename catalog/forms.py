from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Reviews, Rating, RatingStar

class ReviewForm(forms.ModelForm):
    
    captcha = ReCaptchaField()
    
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )
    #print(star)
    class Meta:
        model = Reviews
        fields = ("star", "name", "email", "text", "captcha")
        widgets = {
            
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.TextInput(attrs={"class": "form-control border"}),

         }
        
        

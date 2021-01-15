from django import forms



class CheckoutForm(forms.Form):
    name=forms.CharField(required=True)
    phone=forms.CharField(required=True)
    
    
    
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    override = forms.BooleanField(required=False,
                                    initial=False,
                                    widget=forms.HiddenInput)
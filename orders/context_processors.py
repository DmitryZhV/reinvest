from .models import ProductInBasket
from django.template.context_processors import request

def getting_basket_info(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    
    products_in_basket=ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_num=products_in_basket.count()
    
    return locals()
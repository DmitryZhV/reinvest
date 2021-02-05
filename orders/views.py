from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.template.context_processors import request
from django.http.response import JsonResponse
from orders.models import ProductInBasket, Order, ProductInOrder
from catalog.models import ProductImage, Product
from .cart import Cart
from .forms import CheckoutForm, CartAddProductForm
from django.contrib.auth.models import User
from .tasks import order_created

# Create your views here.


def basket_adding(request):
    return_dict = dict()

    session_key = request.session.session_key
    print(request.POST)
    data=request.POST
    product_id=data.get("product_id")
    nmb=data.get("nmb")
    is_delete = data.get("is_delete")
    is_update = data.get("is_update")
    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)

    else:

        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id, is_active=True, defaults={"num":nmb})
        if not created:
            if  is_update == 'true':
                new_product.num+=int(nmb)
            else:
                new_product.num=int(nmb)
            new_product.save(force_update=True)

    #common code for 2 cases
    product_in_basket=ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    product_total_num=product_in_basket.count()
    print(product_total_num)
    return_dict["product_total_num"]=product_total_num

    return_dict["product"]=list()

    for item in product_in_basket:
        product_dict=dict()
        product_dict["id"]= item.id
        product_dict["name"]= item.product.name
        product_for_image=item.product.id
        print(product_for_image)
        product_image=ProductImage.objects.get( product=product_for_image, is_active=True, is_main=True)
        print(product_image.image)
        product_dict["product_image"]= product_image.image.url
        product_dict["price_per_item"]= item.price_per_item
        product_dict["nmb"]=item.num
        return_dict["product"].append(product_dict)
    #print(return_dict)

    return JsonResponse(return_dict)

def cart(request):
        session_key=request.session.session_key
        products_in_basket=ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
        form=CheckoutForm(request.POST or None)
        if request.POST:
            print(request.POST)
            if form.is_valid():
                print("ok")
                data=request.POST
                name=data.get('name', "111111")#Если пусто будет создано значение
                phone=data['phone'] #Если зачение не вернётся будет ошибка
                user, created=User.objects.get_or_create(username=phone, defaults={"first_name": name})
                order=Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=2)

                for name, value in data.items():
                    if name.startswith("product_"):
                        product_in_basket_id = name.split("product_")[1]
                        product_in_basket=ProductInBasket.objects.get(id=product_in_basket_id)
                        print(type(value))
                        product_in_basket.nmb=value
                        product_in_basket.order=order
                        product_in_basket.save(force_update=True)

                        ProductInOrder.objects.create(product=product_in_basket.product, num=product_in_basket.nmb,
                                                      price_item=product_in_basket.price_per_item,
                                                      total_price=product_in_basket.total_price,
                                                      order=order)


            else:
                print("error")
        return render(request, 'orders/order/cart.html', {'cart': products_in_basket,
                                                                                        })

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'])
    return redirect('orders/cart1.html')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('orders/cart1.html')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    return render(request, 'orders/cart1.html', {'cart': cart})

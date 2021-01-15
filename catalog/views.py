from django.shortcuts import render,get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import JsonResponse, HttpResponse
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import Product, ProductImage, Category, Manufacturer, Reviews
from .forms import ReviewForm

#from django.template.context_processors import request

# Create your views here.

class BrandPrice:
    print("BrandPrice")
    def get_brands(self):
        return Manufacturer.objects.all()

    def get_category(self):
        return Category.objects.all()

   # """"""

def product_main(request):
    categories= Category.objects.all()
    products_buyers=Product.objects.filter(buyers_choice=True)
    products_latest=Product.objects.filter(latest=True)
    products_images = ProductImage.objects.filter(is_active=True, is_main=True)
    print("product_main")
    return render(request, "catalog/product/main.html",
                  {"categories":categories,
                   "products_buyers":products_buyers,
                   "products_latest":products_latest,
                   "products_images":products_images,})

class AddReview(View):
    #
    def get_client_ip(self, request):
        x_forwarder_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarder_for:
            ip = x_forwarder_for.split('.')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk)
        print(request.POST)
        if form.is_valid():
            print("Yes")
            form = form.save(commit=False)
            form.ip = self.get_client_ip(request)
            form.product = product
            form.save()
           
            
           
        return redirect(product.get_absolute_url())


class FilterBrendsView(BrandPrice, ListView):
    """docstring for ."""

    def get_queryset(self):
        categoryN = self.request.GET.getlist("category")
        queryset = Product.objects.filter(
            Q(category__in=self.request.GET.getlist("category"))|
            Q(manufacturer__in=self.request.GET.getlist('brand'))).distinct()
        print(categoryN)
        print(queryset)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        context["manufacturer"] = ''.join([f"manufacturer={x}&" for x in self.request.GET.getlist("manufacturer")])
        return context


class JsonFilterBrendsView(ListView):
    """docstring for ."""

    def get_queryset(self):
        category = Category.objects.get(url=self.kwargs["category_slug"])
        priceList=self.request.GET.getlist('price')
        products = Product.objects.filter(Q(category=category),\
            Q(price__range=self.request.GET.getlist('price')),
            Q(manufacturer__in=self.request.GET.getlist('brand')))\
            .distinct()
        queryset = ProductImage.objects.filter(is_main=True, product__in=products)\
        .values("product__id", "product__category__name", "product__manufacturer__name", "product__name", "product__short_description", "product__price", "product__url", "product__buyers_choice", "image")
        #print(category)
        paginator = Paginator(queryset, 12)
        queryset = paginator.page(1)
        print(queryset)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"products": queryset}, safe=False)

class QuickView(DetailView):


    def quick_view(self):
        product = Product.objects.get( id=self.kwargs["id"])
        queryset = ProductImage.objects.filter(is_main=True, product=product)\
            .values("product__id", "product__name", "product__short_description", "product__price", "product__rest", "product__url", "image")
        print(queryset)
        return queryset

    def get(self,request,  *args, **kwargs):
        queryset = list(self.quick_view())
        return JsonResponse({"product": queryset}, safe=False)

class ProductListView(BrandPrice, ListView):

        model=Product
        queryset = Product.objects.all()

        template_name = 'product/grid.html'


def product_grid( request, category_slug=None):
    #brand = Manufacturer.objects.all().values("id", "name") #.select_related("manufacturer")
    category = get_object_or_404(Category, url=category_slug)
    prodBrand = Product.objects.filter(category=category).select_related('manufacturer').values('manufacturer__id', 'manufacturer__name').distinct()
    #print(category)
    print(prodBrand)
    return_dict = dict()
    return_dict["brand"]=list()
    for item in prodBrand:
        brand_dict=dict()
        brandCount = Product.objects.filter(manufacturer=item['manufacturer__id'], category=category).count()
        brand_dict['id']= item['manufacturer__id']
        brand_dict['name']= item['manufacturer__name']
        brand_dict['count'] = brandCount
        return_dict["brand"].append(brand_dict)
    print(return_dict["brand"])
    brands = Manufacturer.objects.all()
    products=Product.objects.filter(category=category)
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        products = paginator.page(1)
    print(paginator.count)
    categories= Category.objects.all()
    


    return render(request, "catalog/product/grid.html", {"products":products,
                                                "categories":categories,
                                                 "category":category,
                                                 "paginator":paginator,
                                                  "brands": return_dict["brand"],})



def product_detail(request, id, slug):
    
    product= get_object_or_404(Product, id=id, url=slug)
    products = Product.objects.filter(parent=id)
    products_images = ProductImage.objects.filter(product__in = products, is_active=True, is_main=True)
    categories= Category.objects.all()

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()


    print(request.session.session_key)

    return render(request, "catalog/product/detail.html", {"product":product,
                                                    "categories":categories,
                                                    "products":products_images,
                                                    "star_form":ReviewForm(),})

class ParentProducts(ListView):

    def get_queryset(self):

        products = Product.objects.filter(parent=self.kwargs["id"])
        queryset = ProductImage.objects.filter(product__in = products, is_active=True, is_main=True)\
        .values("product__id", "product__name", "product__short_description", "product__price", "product__url", "image")
        print(queryset) 
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"products": queryset}, safe=False)

def product_filter(request, category_slug=None):
    category = Category.objects.get(url=category_slug)
    products=Product.objects.filter(category=category)
    return render(request, "product/grid.html", {"products":products,
                                                    "category":category,})

class Search(ListView):
    """ Поиск товаров """
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get("q"))


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context["q"] = self.request.GET.get("q")
        return context
    
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

from .models import Category, Product, ProductImage, RatingStar, Rating, Reviews, Manufacturer, ProductDetail

#from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label="Полное описание", widget=CKEditorUploadingWidget())
    characteristics = forms.CharField(label="Характиристики", widget=CKEditorUploadingWidget())
    class Meta:
        model = ProductDetail
        fields = '__all__'

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    readonly_fields = ("get_image",)
    
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')
    
    get_image.short_description = "Изображение"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','url']
    prepopulated_fields = {'url': ('name',)}
    
    
    
    class Meta:
        model = Category



@admin.register(Product)    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_description', 'price',
                     'category', 'manufacturer', 'is_active', 'url' ]
    inlines = [ProductImageInline]
    prepopulated_fields = {'url': ('name',)}
    
    #form = ProductAdminForm
    
    class Meta:
        model = Product

class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]
    
    
    
    class Meta:
        model = ProductImage

@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductDetail._meta.fields]
    form = ProductAdminForm

    class Meta:
        model = ProductDetail


admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Reviews)
admin.site.register(Manufacturer)
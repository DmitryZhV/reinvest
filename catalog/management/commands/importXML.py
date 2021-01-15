from django.core.management.base import BaseCommand
from xml.etree import ElementTree
from catalog.models import Category, Product, Manufacturer, ProductImage
from orders.models import ProductInOrder, ProductInBasket
from django.utils.text import slugify
from decimal import Decimal
import shutil




class Command(BaseCommand):
    def handle(self, *args, **options):
        parser = ElementTree.XMLParser(encoding="utf-8")

        productinorder=ProductInOrder.objects.all()
        productinorder.delete()

        productinbasket=ProductInBasket.objects.all()
        productinbasket.delete()

        product=Product.objects.all()
        product.delete()

        category=Category.objects.all()
        category.delete()

        manufacturer=Manufacturer.objects.all()
        manufacturer.delete()


        trans=str.maketrans("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ", "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
        tree = ElementTree.parse("./ImportExport/import.xml", parser=parser)
        root = tree.getroot()
        #print(root)

        
        for element in root.iter("{urn:1C.ru:commerceml_210}Группа"): #Наименование категории
            name=element[1].text
            category=Category(name=name, id1C=element[0].text, url=slugify(name.translate(trans)))
            category.save()
            
        for element in root.iter("{urn:1C.ru:commerceml_210}Свойство"):
            #print(element[1].text)
            for elem in element.iter("{urn:1C.ru:commerceml_210}Справочник"): #Бренд
                name=elem[1].text
                manufact=Manufacturer(name=name, id1C=elem[0].text, slug=slugify(name.translate(trans)))
                manufact.save()
        for element in root.iter("{urn:1C.ru:commerceml_210}Товар"):
            name=element.find("{urn:1C.ru:commerceml_210}Наименование").text
            category=element.find("{urn:1C.ru:commerceml_210}Группы")
            category_id=Category.objects.get(id1C=category[0].text)
            brend=element.find("{urn:1C.ru:commerceml_210}ЗначенияСвойств")
            if brend is not None:
                brend_id=Manufacturer.objects.get(id1C=brend[0][1].text)
            short_description=element.find("{urn:1C.ru:commerceml_210}Описание").text
            country=element.find("{urn:1C.ru:commerceml_210}Страна")
            if country is None:
                country_text=""
            else:
                country_text=country.text
            weight=element.find("{urn:1C.ru:commerceml_210}Вес")
            weight_float=0
            height=0
            width=0
            length=0
            if weight is not None:
                weight_float=Decimal(weight.text)
                
                
            
            for val_req in element.iter("{urn:1C.ru:commerceml_210}ЗначениеРеквизита"):
                if val_req[0].text ==  'Высота':
                    height=Decimal(val_req[1].text)
                elif val_req[0].text ==  'Ширина':
                    width=Decimal(val_req[1].text)
                elif val_req[0].text ==  'Длина':
                    length=Decimal(val_req[1].text)
            #print(name, int(category_id.id), category_id.name, int(brend_id.id), brend_id.name)
            
            product = Product(name=name, id1C=element[0].text, category=category_id, short_description=short_description, country=country_text, weight=weight_float, height=height, width=width, length=length, manufacturer=brend_id, url=slugify(name.translate(trans)))
            product.save()
            #print(element[0].text)
            #print(name)
            img=1
            is_main=True
            if element.find("{urn:1C.ru:commerceml_210}Картинка") is not None:
                for elem in element.iter("{urn:1C.ru:commerceml_210}Картинка"):
                    
                    if elem is not None:
                        #product=Product.objects.get(id1C=element[0].text)
                        name_file=slugify(product.name.translate(trans))+str(img)+".jpg"
                        shutil.copy("./ImportExport/"+elem.text, "./product_images/"+name_file)
                        if img != 1:
                            is_main=False
                        prod_img=ProductImage(product=product, image="product_images/"+name_file, is_main=is_main)
                        prod_img.save()
                        img=img+1
            else:
                prod_img=ProductImage(product=product, image="product_images/no_image.png", is_main=is_main)
                prod_img.save()    

            
        tree = ElementTree.parse("./ImportExport/offers.xml")
        root = tree.getroot()
        for element in root.iter("{urn:1C.ru:commerceml_210}Предложение"):
            #rest_float=0
            product=Product.objects.get(id1C=element[0].text)
            for elem in element.iter("{urn:1C.ru:commerceml_210}Цена"):
                price=elem.find("{urn:1C.ru:commerceml_210}ЦенаЗаЕдиницу")
                if price is not None:
                    product.price=Decimal(price.text)
            rest=element.find("{urn:1C.ru:commerceml_210}Количество")
            if rest is not None:
                product.rest=Decimal(rest.text)
            product.save()
            
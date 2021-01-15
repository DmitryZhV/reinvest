from django.db import models
from datetime import date
from django.urls.base import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField("Категория", max_length=150)
    id1C=models.CharField("Ссылка1С", max_length=64, blank=True, null=True, default=None)
    description = models.TextField("Описание", blank=True, null=True, default=None)
    image = models.ImageField("Изображение", upload_to="category_image/", blank=True)
    url = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    parent = models.ForeignKey(
        'self',  verbose_name="Родитель", on_delete=models.SET_NULL, blank = True, null=True
    )
    is_parent = models.BooleanField("Это родитель", default=False)
    
    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Manufacturer(models.Model):
    name=models.CharField("Бренд", max_length=100)
    id1C=models.CharField("Ссылка1С", max_length=64, blank=True, null=True, default=None)
    image=models.ImageField("Изображение", upload_to='media/manufacturer/', blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
            args=[self.slug])

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Product(models.Model):
    name=models.CharField("Наименование", max_length=64, blank=True, null=True, default=None)
    id1C=models.CharField("Ссылка1С", max_length=64, blank=True, null=True, default=None)
    discount = models.IntegerField("Скидка", default=0 )
    category=models.ForeignKey(Category, verbose_name="Категория", blank=True, null=True, default=None, on_delete=models.CASCADE)
    short_description=models.TextField("Краткое описание", blank=True, null=True, default=None)
    description=models.TextField("Полное описание", blank=True, null=True, default=None)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=0, default=0)
    country = models.CharField("Страна происхождения", max_length=64, blank=True, null=True, default=None)
    weight = models.DecimalField("Вес", max_digits=10, decimal_places=1, default=0)
    height = models.DecimalField("Высота", max_digits=10, decimal_places=1, default=0)
    width = models.DecimalField("Ширина", max_digits=10, decimal_places=1, default=0)
    length = models.DecimalField("Длина", max_digits=10, decimal_places=1, default=0)
    speed = models.DecimalField("Скорость печати", max_digits=10, decimal_places=0, default=0)
    formats = models.CharField("Форматы печати", max_length=64, blank=True, null=True, default=None)
    capacity = models.DecimalField("Емкость лотка", max_digits=10, decimal_places=0, default=0)
    print_type = models.CharField("Тип печати", max_length=64, blank=True, null=True, default=None)
    manufacturer=models.ForeignKey(Manufacturer, verbose_name="Бренд", blank=True, null=True, default=None, on_delete=models.SET_NULL)
    is_active=models.BooleanField("Активен",default=True)
    buyers_choice=models.BooleanField("Выбор_покупателей",default=False)
    latest=models.BooleanField("Последние поступления",default=True)
    created=models.DateTimeField(auto_now_add=True, auto_now=False)
    updated=models.DateTimeField(auto_now_add=False, auto_now=True)
    url = models.SlugField(max_length=130, unique=True)
    rest = models.DecimalField("Остаток", max_digits=10, decimal_places=0, default=0)
    parent =  models.ManyToManyField('self', verbose_name="Сопутствующие товары")
    
    def __str__(self):
        return "%s %s" % (self.price, self.name)

    def get_absolute_url(self):
        return reverse('catalog:product_detail',
            args=[self.id, self.url])

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

# Create your models here.
class ProductImage(models.Model):
    product=models.ForeignKey(Product, verbose_name="Товар", blank=True, null=True, default=None, on_delete=models.CASCADE)
    image=models.ImageField("Изображение", upload_to='product_images/', blank=True)
    is_main=models.BooleanField("Основное изображение", default=False)
    is_active=models.BooleanField("Используется", default=True)
    created=models.DateTimeField(auto_now_add=True, auto_now=False)
    updated=models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product

    def get_absolute_url(self):
        return reverse('catalog:product_detail',
            args=[Product.id, Product.url])

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

class RatingStar(models.Model):
    """docstring for ."""
    value =  models.SmallIntegerField("Значение", default=0)


    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ['-value']

class Rating(models.Model):
    ip = models.CharField("IP адрес", max_length=15)
    star =  models.ForeignKey(RatingStar, verbose_name="звезда", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="товар", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Рейтиг"
        verbose_name_plural = "Рейтиги"

class Reviews(models.Model):
    email = models.EmailField()
    ip = models.CharField("IP адрес", max_length=15)
    name = models.CharField("Имя", max_length=100)
    text =  models.TextField("Сообщение", max_length=5000)
    star =  models.ForeignKey(RatingStar, verbose_name="звезда", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',  verbose_name="Родитель", on_delete=models.SET_NULL, blank = True, null=True
    )
    product = models.ForeignKey(Product, verbose_name="Номенклатура", on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

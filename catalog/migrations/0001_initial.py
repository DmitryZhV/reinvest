# Generated by Django 3.1.3 on 2020-12-21 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Категория')),
                ('id1C', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Ссылка1С')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to='category_image/', verbose_name='Изображение')),
                ('url', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('is_parent', models.BooleanField(default=False, verbose_name='Это родитель')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.category', verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Бренд')),
                ('id1C', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Ссылка1С')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/manufacturer/', verbose_name='Изображение')),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Наименование')),
                ('id1C', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Ссылка1С')),
                ('discount', models.IntegerField(default=0, verbose_name='Скидка')),
                ('short_description', models.TextField(blank=True, default=None, null=True, verbose_name='Краткое описание')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='Полное описание')),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='Цена')),
                ('country', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Страна происхождения')),
                ('weight', models.DecimalField(decimal_places=1, default=0, max_digits=10, verbose_name='Вес')),
                ('height', models.DecimalField(decimal_places=1, default=0, max_digits=10, verbose_name='Высота')),
                ('width', models.DecimalField(decimal_places=1, default=0, max_digits=10, verbose_name='Ширина')),
                ('length', models.DecimalField(decimal_places=1, default=0, max_digits=10, verbose_name='Длина')),
                ('speed', models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='Скорость печати')),
                ('formats', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Форматы печати')),
                ('capacity', models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='Емкость лотка')),
                ('print_type', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Тип печати')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('buyers_choice', models.BooleanField(default=False, verbose_name='Выбор_покупателей')),
                ('latest', models.BooleanField(default=True, verbose_name='Последние поступления')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('url', models.SlugField(max_length=130, unique=True)),
                ('rest', models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='Остаток')),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
                ('manufacturer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.manufacturer', verbose_name='Бренд')),
                ('parent', models.ManyToManyField(related_name='_product_parent_+', to='catalog.Product', verbose_name='Сопутствующие товары')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Звезда рейтинга',
                'verbose_name_plural': 'Звезды рейтинга',
                'ordering': ['-value'],
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('text', models.TextField(max_length=5000, verbose_name='Сообщение')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.reviews', verbose_name='Родитель')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Номенклатура')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15, verbose_name='IP адрес')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='товар')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.ratingstar', verbose_name='звезда')),
            ],
            options={
                'verbose_name': 'Рейтиг',
                'verbose_name_plural': 'Рейтиги',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='product_images/', verbose_name='Изображение')),
                ('is_main', models.BooleanField(default=False, verbose_name='Основное изображение')),
                ('is_active', models.BooleanField(default=True, verbose_name='Используется')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Изображение товара',
                'verbose_name_plural': 'Изображения товаров',
            },
        ),
    ]

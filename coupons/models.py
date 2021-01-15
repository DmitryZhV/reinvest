from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Coupon(models.Model):
    code = models.CharField("Код", max_length=50,
                                unique=True)
    valid_from = models.DateTimeField("Дата начала")
    valid_to = models.DateTimeField("Дата окончания")
    discount = models.IntegerField(
                        validators=[MinValueValidator(0),
                                    MaxValueValidator(100)])
    active = models.BooleanField("Активность")
    
    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'
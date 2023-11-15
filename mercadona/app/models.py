from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name
    
def validate_discount_percentage(value):
    if value <= 0 or value >= 100:
        raise ValidationError('The discount percentage must be strictly greater than 0 and less than 100.')

def validate_price(value):
    if value <= 0:
        raise ValidationError('The price must be strictly greater than 0.')
    

class Product(models.Model):    
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category, related_name='products')
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products/", blank=True, null=True)
    thumbnail_title = models.CharField(max_length=100, blank=True)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2,validators=[validate_price])
    
    def __str__(self):
            return f'{self.name}' 

class Discount(models.Model):
    discount_percentage = models.DecimalField(max_digits=3, decimal_places=0, validators=[validate_discount_percentage])
    start_date = models.DateField()
    end_date = models.DateField()
    product = models.OneToOneField(Product, on_delete=models.CASCADE, default=None)
    discounted_price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    active = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.discount_percentage}% off for {self.product}'

    def clean(self):
        super().clean()

        # Verify if start_date is greater than end_date
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({'start_date': ('The start date must be before the end date.')})

    @property
    def is_discount_active(self):
        today = timezone.now().date()
        return self.start_date and self.end_date and self.start_date <= today <= self.end_date

    def save(self, *args, **kwargs):
        # Call the clean method before saving to perform the verification
        self.clean()
        # Set the active attribute based on the is_discount_active property
        self.active = self.is_discount_active
        super().save(*args, **kwargs)

    def calculate_discounted_price(self):
        if self.discount_percentage is not None and self.product is not None:
            self.discounted_price = self.product.initial_price - (
                self.product.initial_price * (self.discount_percentage / 100)
            )
        else:
            self.discounted_price = None

@receiver(pre_save, sender=Discount)
def discount_pre_save(sender, instance, **kwargs):
    instance.calculate_discounted_price()
    
    
@receiver(pre_save, sender=Discount)
def discount_pre_save(sender, instance, **kwargs):
    instance.calculate_discounted_price()
    
    
class Homepage(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to="home", blank=True, null=True)
    image_title = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.name} update : images and texts'
    
class Event(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to="home", blank=True, null=True)
    image_title = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} update : images and texts'

    




    



from abc import abstractmethod, ABC

from django.db import models

from django.conf import settings
from .utils import *


# Create your model here
class SuperModel(models.Model):
    id = models.CharField(primary_key=True, unique=True, editable=False, blank=True, max_length=30)
    addDate = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        while not self.id:
            newId = get_random_alphanumeric_string(20)

            if not __class__(self).objects.filter(pk=newId).exists():
                self.id = newId
        super(SuperModel, self).save()

    class Meta:
        abstract = True


class Product(SuperModel):
    class StockUnit(models.TextChoices):
        UNIT = 'UNIT'
        KILOGRAM = 'KILOGRAM'
        LITER = 'LITER'

    name = models.CharField(max_length=60)
    description = models.CharField(max_length=1500)
    unitPrice = models.FloatField()
    stockUnit = models.CharField(max_length=20, choices=StockUnit.choices, default=StockUnit.UNIT)
    stockQuantity = models.FloatField()
    alertThreshold = models.IntegerField()

    def __str__(self):
        return self.name


class Command(SuperModel):
    commandDate = models.DateTimeField(auto_now_add=True)
    totalPrice = models.FloatField(default="")
    products = models.ManyToManyField(Product, through='CommandRow', related_name='commands')
    command_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")

    def __str__(self):
        return 'Commanded by: ' + self.command_by.name


class CommandRow(SuperModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    command = models.ForeignKey(Command, on_delete=models.CASCADE, default="")
    quantityOrdered = models.IntegerField()


class Delivery(SuperModel):
    deliveryDate = models.DateTimeField(auto_now_add=True)
    commandRows = models.ManyToManyField(CommandRow, through='DeliveryDetails', related_name='deliveries')
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    totalProductDelivered = models.IntegerField()


class DeliveryDetails(SuperModel):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, default="")
    commandRow = models.ForeignKey(CommandRow, on_delete=models.CASCADE, default="")
    quantityDelivered = models.IntegerField()

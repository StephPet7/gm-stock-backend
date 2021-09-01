from abc import abstractmethod, ABC

from django.db import models

from django.conf import settings
from .utils import *


class Product(models.Model):
    class StockUnit(models.TextChoices):
        U = 'U'
        FF = 'FF'
        ml = 'ml'
        m2 = 'm2'
        m3 = 'm3'
        L = 'L'

    id = models.CharField(primary_key=True, unique=True,
                          editable=False, blank=True, max_length=30)
    addDate = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=1500, default="")
    unitPrice = models.FloatField()
    stockUnit = models.CharField(
        max_length=20, choices=StockUnit.choices, default=StockUnit.U)
    stockQuantity = models.FloatField()
    alertThreshold = models.IntegerField()

    def save(self, *args, **kwargs):
        while not self.id:
            newId = get_random_alphanumeric_string(20)

            if not Product.objects.filter(pk=newId).exists():
                self.id = newId
        super(Product, self).save()

    def __str__(self):
        return self.name


class Command(models.Model):
    id = models.CharField(primary_key=True, unique=True,
                          editable=False, blank=True, max_length=30)
    addDate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, default="")
    commandDate = models.DateTimeField(auto_now_add=True)
    totalPrice = models.FloatField(default="")
    products = models.ManyToManyField(
        Product, through='CommandRow', related_name='commands')
    command_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")

    def save(self, *args, **kwargs):
        while not self.id:
            newId = get_random_alphanumeric_string(20)

            if not Command.objects.filter(pk=newId).exists():
                self.id = newId
        super(Command, self).save()

    def __str__(self):
        return 'Commanded by: ' + self.command_by.name


class CommandRow(models.Model):
    id = models.CharField(primary_key=True, unique=True,
                          editable=False, blank=True, max_length=30)
    addDate = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    command = models.ForeignKey(Command, on_delete=models.CASCADE, default="")
    quantityOrdered = models.IntegerField()
    remaining = models.IntegerField()

    def save(self, *args, **kwargs):
        while not self.id:
            newId = get_random_alphanumeric_string(20)

            if not CommandRow.objects.filter(pk=newId).exists():
                self.id = newId
        super(CommandRow, self).save()


class Delivery(models.Model):
    id = models.CharField(primary_key=True, unique=True,
                          editable=False, blank=True, max_length=30)
    addDate = models.DateTimeField(auto_now_add=True)
    deliveryDate = models.DateTimeField(auto_now_add=True)
    commandRows = models.ManyToManyField(
        CommandRow, through='DeliveryDetails', related_name='deliveries')
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    totalProductDelivered = models.IntegerField()

    def save(self, *args, **kwargs):
        while not self.id:
            newId = get_random_alphanumeric_string(20)

            if not Delivery.objects.filter(pk=newId).exists():
                self.id = newId
        super(Delivery, self).save()


class DeliveryDetails(models.Model):
    id = models.CharField(primary_key=True, unique=True,
                          editable=False, blank=True, max_length=30)
    delivery = models.ForeignKey(
        Delivery, on_delete=models.CASCADE, default="")
    commandRow = models.ForeignKey(
        CommandRow, on_delete=models.CASCADE, default="")
    quantityDelivered = models.IntegerField()
    addDate = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        while not self.id:
            newId = get_random_alphanumeric_string(20)

            if not DeliveryDetails.objects.filter(pk=newId).exists():
                self.id = newId
        super(DeliveryDetails, self).save()

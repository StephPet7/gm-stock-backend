from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id',
                  'name',
                  'description',
                  'unitPrice',
                  'stockUnit',
                  'stockQuantity',
                  'alertThreshold')


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ('id',
                  'commandDate',
                  'totalPrice',
                  'command_by')


class CommandRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandRow
        fields = ('id',
                  'product',
                  'command',
                  'quantityOrdered')


class DeliverySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Delivery
        fields = ('id',
                  'deliveryDate',
                  'received_by')


class DeliveryDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeliveryDetails
        fields = ('id',
                  'delivery',
                  'commandRow',
                  'quantityDelivered')

from rest_framework import serializers
from .models import *
from users.serializers import RegisterUserSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id',
                  'name',
                  'description',
                  'unitPrice',
                  'stockUnit',
                  'stockQuantity',
                  'alertThreshold',
                  'addDate')
        extra_kwargs = {'addDate': {'read_only': True}}


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ('id',
                  'title',
                  'commandDate',
                  'totalPrice',
                  'command_by')
        extra_kwargs = {'addDate': {'read_only': True}}


class CommandRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandRow
        fields = ('id',
                  'product',
                  'command',
                  'quantityOrdered',
                  'remaining')
        extra_kwargs = {'addDate': {'read_only': True}}


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('id',
                  'deliveryDate',
                  'received_by')
        extra_kwargs = {'addDate': {'read_only': True}}


class DeliveryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryDetails
        fields = ('id',
                  'delivery',
                  'commandRow',
                  'quantityDelivered')
        extra_kwargs = {'addDate': {'read_only': True}}

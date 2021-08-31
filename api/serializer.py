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
    command_by = RegisterUserSerializer(many=False)

    class Meta:
        model = Command
        fields = ('id',
                  'commandDate',
                  'totalPrice',
                  'command_by')
        extra_kwargs = {'addDate': {'read_only': True}}


class CommandRowSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    command = CommandSerializer(many=False)

    class Meta:
        model = CommandRow
        fields = ('id',
                  'product',
                  'command',
                  'quantityOrdered')
        extra_kwargs = {'addDate': {'read_only': True}}


class DeliverySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Delivery
        fields = ('id',
                  'deliveryDate',
                  'received_by')
        extra_kwargs = {'addDate': {'read_only': True}}


class DeliveryDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeliveryDetails
        fields = ('id',
                  'delivery',
                  'commandRow',
                  'quantityDelivered')
        extra_kwargs = {'addDate': {'read_only': True}}

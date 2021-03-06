# Create your serializers here
from rest_framework import serializers

from users.models import *


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'user_name', 'password',
                  'role', 'name', 'is_active', 'addDate']
        extra_kwargs = {'password': {'read_only': True}}

    def create(self, validated_data):
        password = get_random_alphanumeric_string(7)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return (instance, password)

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."})
        instance.name = validated_data['name']
        instance.role = validated_data['role']
        instance.email = validated_data['email']
        instance.user_name = validated_data['user_name']
        instance.save()
        return instance

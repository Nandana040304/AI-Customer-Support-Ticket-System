from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Ticket


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):

        # check email format (basic)
        if "@" not in value:
            raise serializers.ValidationError("Invalid email format")

        # check duplicate email
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")

        return value

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user
class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'
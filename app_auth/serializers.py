# pylint: disable=missing-docstring
# pylint: disable=missing-final-newline

from rest_framework import serializers
from app_auth.models import Account

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'fullname', 'password', 'date_joined']
        extra_kwargs={
            'password': {'write_only':True},
        }
    def create(self, validate_data):
        return Account.objects.create_user(**validate_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'fullname']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    class Meta:
        model = Account
        fields = ['email', 'password']
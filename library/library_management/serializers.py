from rest_framework import serializers
from .models import AddBooks, Barrow
from django.contrib.auth.models import User

from rest_framework import serializers
from .models import AddBooks

class BookSerializeers(serializers.ModelSerializer):
    class Meta:
        model = AddBooks
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'availability_status']
        
    def create(self, validated_data):
        validated_data.setdefault('availability_status', 'available')
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
    

class BorrowSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    book = BookSerializeers(read_only=True)

    class Meta:
        model = Barrow
        fields = ['user', 'book', 'borrow_date', 'return_date', 'is_returned']
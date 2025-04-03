from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Department, Issue, Category, Registration, Activity

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def validate(self, data):
        # Check if email or username already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        
        # Validate password matching and strength
        self.validate_password_strength(data['password'], data['confirm_password'])
        
        return data
    
    def validate_password_strength(self, password, confirm_password):
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        if len(password) < 8:
            raise serializers.ValidationError({'password': 'Password must be at least 8 characters'})
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError({'password': 'Password must contain at least one number.'})
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError({'password': 'Password must contain at least one uppercase letter.'})

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, max_length

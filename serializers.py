from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Department, Issue,Category, Registration,Activity# Import  model

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password'
        ]
        
    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        
        if len(data['password']) < 8:
            raise serializers.ValidationError({'password': 'Password must be at least 8 characters'})
        
        # Add password complexity validation
        if not any(char.isdigit() for char in data['password']):
            raise serializers.ValidationError({'password': 'Password must contain at least one number.'})
        if not any(char.isupper() for char in data['password']):
            raise serializers.ValidationError({'password': 'Password must contain at least one uppercase letter.'})

        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_user = User.objects.create_user(**validated_data)
        return validated_user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('Invalid credentials')  # Generic error message
                return user
            else:
                raise serializers.ValidationError('Invalid credentials')  # Generic error message
        else:
            raise serializers.ValidationError('Must include "email" and "password"')

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email address.")
        return value

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'department', 'user', 'status', 'created_at', 'updated_at','assigned_to','affected_course','affected_student']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']
        def validate_title(self, value):
            if len(value) < 10:
                raise serializers.ValidationError("Title must be at least 10 characters ")
            return value
        def validate_description(self, value):
            if len(value) < 20:
                raise serializers.ValidationError("Description must be at least 20 characters ")
            return value
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']
    
class ActivitySerializer(serializers.ModelSerializer):
    user = IssueSerializer(read_only=True)
    class Meta:
        model = Activity
        fields = ['id', 'issue', 'action', 'created_at']
        read_only_fields = ['timestamp']
        

    

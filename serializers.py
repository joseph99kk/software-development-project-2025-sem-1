from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Department, Issue, Category, Registration, Activity
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()
#class registration

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        validators = [
            UniqueValidator(queryset=User.objects.all(), field='email', message=_("Email already exists")),
            UniqueValidator(queryset=User.objects.all(), field='username', message=_("Username already exists"))
        ]
        
    def validate_password(self, value):
        
        if len(value) < 8:
            raise serializers.ValidationError(_("Password must be at least 8 characters"))
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(_("Password must contain at least one number"))
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(_("Password must contain at least one uppercase letter"))
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': _('Passwords do not match')})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError(_('Must include "email" and "password"'))

        user = authenticate(email=email, password=password)
        if user:
            if not user.is_active:
                raise serializers.ValidationError(_('Invalid credentials'))
            return user
        raise serializers.ValidationError(_('Invalid credentials'))


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No user is associated with this email address."))
        return value


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        return self.validate_password(value)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": _("Old password is incorrect.")})
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
        fields = ['Issue_id', 'title', 'description', 'category', 'department', 'user', 'status', 'created_at', 'updated_at', 'assigned_to', 'affected_course', 'affected_student']
        read_only_fields = ['Issue_id', 'user', 'status', 'created_at', 'updated_at']

    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(_("Title must be at least 10 characters"))
        return value

    def validate_description(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(_("Description must be at least 20 characters"))
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']


class ActivitySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'issue', 'user', 'user_name', 'action', 'details', 'timestamp']
        read_only_fields = ['timestamp']


class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField(max_length=500)


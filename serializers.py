from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Department, Issue, Category, Registration, Activity
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def validate_password_strength(password):
    """Validates password security requirements."""
    if len(password) < 8:
        raise serializers.ValidationError(_("Password must be at least 8 characters long."))
    if not any(char.isdigit() for char in password):
        raise serializers.ValidationError(_("Password must contain at least one number."))
    if not any(char.isupper() for char in password):
        raise serializers.ValidationError(_("Password must contain at least one uppercase letter."))
    return password


# User Registration Serializer
class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Email already exists."))
        return value

    def validate_password(self, value):
        """Validate password security."""
        return validate_password_strength(value)

    def validate(self, data):
        """Ensure password and confirm password match."""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': _("Passwords do not match.")})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


# User Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate user with email and password."""
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError(_('Invalid credentials or user does not exist.'))

        if not user.is_active:
            raise serializers.ValidationError(_('User account is inactive.'))

        data['user'] = user
        return data


# Password Reset Serializer
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if user exists for the provided email."""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No user is associated with this email address."))
        return value


# Password Change Serializer
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        """Ensure strong password."""
        return validate_password_strength(value)

    def validate(self, data):
        """Check if old password is correct."""
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": _("Old password is incorrect.")})
        return data

    def save(self, **kwargs):
        """Set new password and save user."""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


# Department Serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']


# Issue Serializer
class IssueSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True)

    class Meta:
        model = Issue
        fields = [
            'issue_id', 'title', 'description', 'category', 'department', 'user', 'user_email',
            'status', 'created_at', 'updated_at', 'assigned_to', 'assigned_to_email', 'affected_course', 'affected_student'
        ]
        read_only_fields = ['issue_id', 'user', 'status', 'created_at', 'updated_at']

    def validate_title(self, value):
        """Ensure title is descriptive enough."""
        if len(value) < 10:
            raise serializers.ValidationError(_("Title must be at least 10 characters."))
        return value

    def validate_description(self, value):
        """Ensure description provides enough detail."""
        if len(value) < 20:
            raise serializers.ValidationError(_("Description must be at least 20 characters."))
        return value


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']


# Activity Serializer
class ActivitySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'issue', 'user', 'user_name', 'action', 'details', 'timestamp']
        read_only_fields = ['timestamp']


# Contact Form Serializer
class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField(max_length=500)



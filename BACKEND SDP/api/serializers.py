# api/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Issue, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'registration_number']
        read_only_fields = ['id']
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role', 'registration_number']
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user', 'user_name', 'user_role']
        read_only_fields = ['id', 'created_at']
        
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
        
    def get_user_role(self, obj):
        return obj.user.role

class IssueSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    student_name = serializers.SerializerMethodField()
    lecturer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Issue
        fields = ['id', 'title', 'course_code', 'details', 'status', 'priority',
                'created_at', 'updated_at', 'student', 'lecturer',
                'student_name', 'lecturer_name', 'comments']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
        
    def get_lecturer_name(self, obj):
        if obj.lecturer:
            return f"{obj.lecturer.first_name} {obj.lecturer.last_name}"
        return None

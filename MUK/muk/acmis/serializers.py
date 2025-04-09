from rest_framework import serializers
from .models import User , Student , Lecturer,Course ,Admin ,Registrar

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ['id','username','email','role']
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        field = '__all__'
        
class LecturerSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Lecturer
        field = '__all__'
        
class AdminSerializer(serializers.ModelSerializer):
       class Meta:
        model = Admin
        field = '__all__'
        
        
class RegistrarSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Registrar
        field = '__all__'
        
        
class CourseSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Course
        field = '__all__'
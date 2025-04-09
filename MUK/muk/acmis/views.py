from django.shortcuts import render
from rest_framework import viewsets
from .models import Student ,Lecturer,Course,Registrar,Admin
from .serializers import StudentSerializer,LecturerSerializer,CourseSerializer,RegistrarSerializer,AdminSerializer
from django.http import JsonResponse
# Create your views here.
def api_home(request):
    return JsonResponse({"messgae":"Welcome to the academic Management System"})

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class RegistrarViewSet(viewsets.ModelViewSet):
    queryset = Registrar.objects.all()
    serializer_class = RegistrarSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

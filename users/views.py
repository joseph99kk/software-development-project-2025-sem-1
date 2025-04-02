from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views import View
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .forms import RegistrationForm
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .permissions import IsStudent, IsLecturer, IsRegistrar, IsAdmin
from rest_framework.views import APIView

User = get_user_model()

# User Registration View (for rendering registration page and handling the post request)
class RegisterPageView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash password
            user.save()  # Save the user without logging them in
            return redirect('login')  # Redirect to the login page
        return render(request, "users/register.html", {"form": form})
# Custom Login View to handle role-based redirection after login
class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        # Redirect based on the role of the user
        if self.request.user.role == "Student":
            return redirect("student_portal")
        elif self.request.user.role == "Lecturer":
            return redirect("lecturer_portal")
        elif self.request.user.role == "Registrar":
            return redirect("registrar_portal")
        elif self.request.user.role == "Admin":
            return redirect("admin_portal")
        return super().get_success_url()

# Role-based Views

class StudentOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        return Response({"message": "Welcome, student!"})

class LecturerOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsLecturer]

    def get(self, request):
        return Response({"message": "Welcome, lecturer!"})

class RegistrarOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsRegistrar]

    def get(self, request):
        return Response({"message": "Welcome, registrar!"})

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Welcome, admin!"})

# API Views for Registering and Logging In (JWT)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializer, LoginSerializer, PasswordResetSerializer, PasswordChangeSerializer, DepartmentSerializer, IssueSerializer, CategorySerializer,ActivitySerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets  # Correct import for ModelViewSet
from .models import Department, Issue, Category
from.permissions import IsOwnerOrStaff
# Create your views here.
User = get_user_model()

class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "User registered successfully", "user": response.data}, status=status.HTTP_201_CREATED)

class LoginView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    pass

class MyTokenRefreshView(TokenRefreshView):
    pass

class PasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentListCreateView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class DepartmentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class IssueListCreateView(ListCreateAPIView):#API endpoints to submit issues
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IssueDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrStaff]

class CategoryViewSet(viewsets.ModelViewSet):  # Corrected usage of ModelViewSet
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        category = serializer.save()
        # Log activity for category creation
        Activity.objects.create(
            issue=None,  # Replace with an actual issue instance if applicable
            user=self.request.user,
            action='created',
            details=f'Category "{category.name}" was created.'
        )

    def perform_update(self, serializer):
        category = serializer.save()
        # Log activity for category update
        Activity.objects.create(
            issue=None,  # Replace with an actual issue instance if applicable
            user=self.request.user,
            action='updated',
            details=f'Category "{category.name}" was updated.'
        )
    
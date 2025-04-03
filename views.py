from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordChangeSerializer,
    DepartmentSerializer,
    IssueSerializer,
    CategorySerializer,
    ActivitySerializer,
    ContactFormSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets  # Correct import for ModelViewSet
from .models import Department, Issue, Category, Activity
from .permissions import IsOwnerOrStaff
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
User = get_user_model()


class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "message": "User registered successfully",
                "user": response.data,
            },
            status=status.HTTP_201_CREATED,
        )


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
            return Response(
                {"message": "Password reset email sent."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password changed successfully."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentListCreateView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class DepartmentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class IssueListCreateView(ListCreateAPIView):  # API endpoints to submit issues
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IssueDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]


class CategoryViewSet(viewsets.ModelViewSet):  
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        category = self.request.data.get('category')
        if not category:
            
            return Response({'category': "Category name is required."})
                            
        serializer.save(created_by=self.request.user)
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


class ContactFormView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            # Process the form data (e.g., send an email)
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']

            # Example: Send an email
            subject = f"New Contact Form Submission from {name}"
            email_message = (
                f"Name: {name}\n"
                f"Email: {email}\n\n"
                f"Message:\n{message}"
            )
            try:
                send_mail(
                    subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['codewithlynah.com'], 
                    fail_silently=False,
                )
                return Response({"message": "Form submitted successfully."}, 
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Add to views.py:


class ActivityListView(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        This view should return a list of all activities,
        but it can be filtered by issue_id if provided.
        """
        queryset = Activity.objects.all()
        issue_id = self.request.query_params.get('issue_id', None)
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset
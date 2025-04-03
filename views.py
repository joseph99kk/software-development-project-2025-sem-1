from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializer, LoginSerializer, PasswordResetSerializer, PasswordChangeSerializer, ContactFormSerializer, DepartmentSerializer, IssueSerializer, CategorySerializer, ActivitySerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets  # Correct import for ModelViewSet
from .models import Department, Issue, Category, Activity
from .permissions import IsOwnerOrStaff
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


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
            user = User.objects.filter(email=serializer.validated_data['email']).first()
            if user:
                reset_link = request.build_absolute_uri(
                    reverse('password-reset-confirm', kwargs={'uid': user.pk, 'token': 'dummy-token'})
                )
                subject = "Password Reset Request"
                message = f"Click the link below to reset your password:\n\n{reset_link}"
                recipient_list = [user.email]
                try:
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)
                    return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

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


class IssueListCreateView(ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        issue = serializer.save(user=self.request.user)
        # Log activity for issue creation
        Activity.objects.create(
            issue=issue,
            user=self.request.user,
            action='created',
            details=f'Issue "{issue.title}" was created.'
        )


class IssueDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]

    def perform_update(self, serializer):
        issue = serializer.save()
        # Log activity for issue update
        Activity.objects.create(
            issue=issue,
            user=self.request.user,
            action='updated',
            details=f'Issue "{issue.title}" was updated.'
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        category = serializer.save()
        # Log activity for category creation
        Activity.objects.create(
            issue=None,  # No associated issue for category creation
            user=self.request.user,
            action='created',
            details=f'Category "{category.name}" was created.'
        )

    def perform_update(self, serializer):
        category = serializer.save()
        # Log activity for category update
        Activity.objects.create(
            issue=None,  # No associated issue for category update
            user=self.request.user,
            action='updated',
            details=f'Category "{category.name}" was updated.'
        )


class ContactFormView(APIView):
    def post(self, request, *args, **kwargs):
        # Placeholder for actual contact form submission logic
        title = request.data.get('title')
        course_code = request.data.get('coursecode')
        details = request.data.get('details')
        return Response({"message": "Issue submitted successfully."}, status=status.HTTP_200_OK)


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




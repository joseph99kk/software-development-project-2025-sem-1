from django.urls import path
from .views import (
    RegistrationView, LoginView, MyTokenObtainPairView, MyTokenRefreshView,
    PasswordResetView, PasswordChangeView,
    DepartmentListCreateView, DepartmentDetailView,
    IssueListCreateView, IssueDetailView,
)

app_name = 'UNI'

urlpatterns = [
    # User registration
    path('register/', RegistrationView.as_view(), name='register'),

    # User login
    path('login/', LoginView.as_view(), name='login'),

    # JWT token authentication
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),

    # Password reset (e.g., via email)
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),

    # Password change for authenticated users
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),

    # Department endpoints
    path('departments/', DepartmentListCreateView.as_view(), name='department_list_create'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department_detail'),

    # Issue endpoints
    path('issues/', IssueListCreateView.as_view(), name='issue_list_create'),
    path('issues/<int:pk>/', IssueDetailView.as_view(), name='issue_detail'),

]
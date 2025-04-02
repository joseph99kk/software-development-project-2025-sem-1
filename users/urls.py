from django.urls import path
from .views import RegisterView, LoginView, StudentOnlyView, LecturerOnlyView, RegistrarOnlyView, AdminOnlyView
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.views import LogoutView
from .views import RegisterPageView
from . import views

urlpatterns = [
    path('register/', views.RegisterPageView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('student-portal/', StudentOnlyView.as_view(), name='student_portal'),
    path('lecturer-portal/', LecturerOnlyView.as_view(), name='lecturer_portal'),
    path('registrar-portal/', RegistrarOnlyView.as_view(), name='registrar_portal'),
    path('admin-portal/', AdminOnlyView.as_view(), name='admin_portal'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('student/', StudentOnlyView.as_view(), name='student-only'),
    path('lecturer/', LecturerOnlyView.as_view(), name='lecturer-only'),
    path('registrar/', RegistrarOnlyView.as_view(), name='registrar-only'),
    path('admin/', AdminOnlyView.as_view(), name='admin-only'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
     path("api/register/", RegisterView.as_view(), name="register"),  # ✅ This handles API registration
    path("api/login/", LoginView.as_view(), name="login"),
]

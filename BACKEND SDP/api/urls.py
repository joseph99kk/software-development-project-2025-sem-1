from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('signup/', views.sign_up),
    path('login/', views.login),
    path('update_profile/<str:pk>', views.update_profile),
    path('courses/<str:pk>', views.courses),
    path('all_courses/<str:pk>', views.all_courses),
    path('programmes/', views.programmes),
    path('lecturers/', views.lecturers),
    path('student_statistics/<str:pk>', views.student_statistics),
    path('notifications/<str:pk>', views.notifications),
    path('view_notifications/<str:pk>', views.view_notifications),
    path('academic_years/', views.academic_years),
    path('registration_issues/<str:pk>', views.registration_issues),
    path('missing_marks/<str:pk>', views.missing_marks),
    path('sent_complaints/<str:pk>', views.sent_complaints),
    path('reg_complaints/<str:pk>', views.reg_complaints),
    path('update_reg_complaint/<str:pk>', views.update_reg_complaint),
    path('update_marks_complaint/<str:pk>', views.update_marks_complaint),
    path('marks_complaints/<str:pk>', views.marks_complaints),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
]


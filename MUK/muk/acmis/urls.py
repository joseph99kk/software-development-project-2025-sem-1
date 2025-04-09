from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, LecturerViewSet, CourseViewSet, RegistrarViewSet, AdminViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'lecturers', LecturerViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'Registrar', RegistrarViewSet)
router.register(r'Admin', AdminViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

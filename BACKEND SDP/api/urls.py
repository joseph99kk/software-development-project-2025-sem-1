# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'issues', views.IssueViewSet, basename='issue')

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/', views.CustomAuthToken.as_view(), name='token_auth'),
    path('register/', views.register_user, name='register'),
    path('users/me/', views.current_user, name='current_user'),
    path('issues/<int:issue_id>/comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='issue_comments'),
    path('issues/<int:issue_id>/comments/<int:pk>/', views.CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='comment_detail'),
]


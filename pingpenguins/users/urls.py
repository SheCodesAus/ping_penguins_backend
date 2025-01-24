
from django.urls import path
from . import views
from .views import CustomUserList, CustomUserDetail, CustomAuthToken

urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('users/<int:pk>/', views.CustomUserDetail.as_view()),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api-token-auth'),
    path('public-users/<int:pk>/', views.PublicUserDetail.as_view()),
    ]
from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.BoardList.as_view()),
    # path('board/<int:pk>/', views.BoardDetail.as_view()), This is to be updated once UUID functionality added
    path('category/', views.CategoryList.as_view())
    ]
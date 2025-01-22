from django.urls import path
from .import views

urlpatterns = [
    path('board/', views.BoardList.as_view()),
    path('board/<int:code>/', views.BoardDetail.as_view()),
    path('category/', views.CategoryList.as_view()),
    path('note/', views.NoteList.as_view()),
    # path('note/<int:pk>/', views.CategoryDetail.as_view())  This is to be updated once note functionality added
    ]
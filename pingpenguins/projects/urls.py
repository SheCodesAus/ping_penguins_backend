from django.urls import path
from .import views

urlpatterns = [
    path('board/', views.BoardList.as_view()),
    path('board/<uuid:code>/', views.BoardDetail.as_view()), 
    path('category/', views.CategoryList.as_view()),
    path('note/', views.NoteList.as_view()),
    path('note/<int:pk>/', views.NoteDetail.as_view())
    ]
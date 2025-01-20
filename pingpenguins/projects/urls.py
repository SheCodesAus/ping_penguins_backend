from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.BoardList.as_view()),
    ]
from django.db import models
from django.contrib.auth import get_user_model

class Board(models.Model):
    title = models.CharField(max_length=200) # Char limit 200
    description = models.TextField()
    disclaimer = models.TextField(blank=True) # Optional empty
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    image = models.URLField(blank=True) # Optional empty
    code = models.UUIDField(unique=True) # Unique constraint
    created_at = models.DateTimeField(auto_now_add=True) # Stores created datetimestamp for backend db reference

class Category(models.Model):
    title = models.CharField(max_length=200)
    board = models.ForeignKey(
        'Board',
        on_delete=models.CASCADE,
        related_name='categories'
    )
    class Meta:
        verbose_name_plural = "categories" # Overruling Django's default naming of categorys after adding plural s

class Note(models.Model):
    comment = models.CharField(max_length=200) # Char limit 200
    anonymous = models.BooleanField(default=False) # Default false
    created_at = models.DateTimeField(auto_now_add=True) # Stores created datetimestamp for backend db reference
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='notes'
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_notes'
    )

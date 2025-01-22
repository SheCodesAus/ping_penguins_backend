from rest_framework import serializers
from django.apps import apps

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('projects.Note')
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)
    
    class Meta:
        model = apps.get_model('projects.Category')
        fields = '__all__'

class BoardSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = apps.get_model('projects.Board')
        fields = '__all__'
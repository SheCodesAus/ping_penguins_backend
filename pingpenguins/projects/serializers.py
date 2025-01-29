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

class BoardDetailSerializer(BoardSerializer):
    notes = NoteSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.disclaimer = validated_data.get('disclaimer', instance.disclaimer)
        instance.date_start = validated_data.get('date_start', instance.date_start)
        instance.date_end = validated_data.get('date_end', instance.date_end)
        instance.image = validated_data.get('image', instance.image)
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return instance
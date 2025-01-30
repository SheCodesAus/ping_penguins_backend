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

class BoardCategorySerializer(CategorySerializer):
    board = serializers.ReadOnlyField(source='board.id')

class BoardSerializer(serializers.ModelSerializer):
    categories = BoardCategorySerializer(many=True, required=False)  # Allow categories to be empty

    class Meta:
        model = apps.get_model('projects.Board')
        fields = '__all__'

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        board = apps.get_model('projects.Board').objects.create(**validated_data)
        for category_data in categories_data:
            apps.get_model('projects.Category').objects.create(board=board, **category_data)
        return board

class BoardDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)  # Read-only nested categories

    class Meta:
        model = apps.get_model('projects.Board')
        fields = '__all__'

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
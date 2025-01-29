from rest_framework import serializers
from .models import Board, Category, Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True) 

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        notes_data = validated_data.pop('notes', [])
        category = Category.objects.create(**validated_data)
        for note_data in notes_data:
            Note.objects.create(category=category, **note_data)
        return category

class BoardSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=False)  # Allow categories to be empty

    class Meta:
        model = Board
        fields = '__all__'

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])  # Default to empty list if no categories
        board = Board.objects.create(**validated_data)
        for category_data in categories_data:
            category_data['board'] = board  # Set the board field for each category
            Category.objects.create(**category_data)
        return board

class BoardDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)  # Read-only nested categories

    class Meta:
        model = Board
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
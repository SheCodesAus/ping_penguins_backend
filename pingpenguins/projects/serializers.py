from rest_framework import serializers
from django.apps import apps
from users.serializers import PublicUserSerializer
from .models import Board, Category, Note

class NoteSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(read_only=True)  # Make sure 'board' is read-only if you don't want it to be set
    owner = PublicUserSerializer(read_only=True)
    
    class Meta:
        model = Note
        fields = '__all__'

    def validate_category(self, value):
        request = self.context.get('request')
        if request:
            board_id = request.data.get('board')
            if board_id and str(value.board.id) != str(board_id):
                raise serializers.ValidationError("Category does not belong to the specified board")
        return value

    def create(self, validated_data):
        # Automatically set the owner to the logged-in user
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['owner'] = request.user  # Assign logged-in user to the note owner
        return super().create(validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['board'] = instance.category.board.id  
        return ret
    
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
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
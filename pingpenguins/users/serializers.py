from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'password', 'confirm_password', 
            'first_name', 'last_name', 'display_name', 'position', 
            'gender', 'tenure', 'age', 'sticky_note_colour'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'display_name': {'required': True},
            'sticky_note_colour': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return CustomUser.objects.create_user(**validated_data)
    
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['display_name']
    def to_representation(self, instance):
        # Access the request object from the context to check if the user is authenticated
        request = self.context.get('request')

        # If the user is not authenticated, raise a PermissionDenied exception or return a custom message
        if not request.user.is_authenticated:
            raise PermissionDenied(detail="You are not authorized to view this content.")  # Raise Unauthorized error
        
        # If the user is authenticated, return the original representation (display_name)
        return super().to_representation(instance)   
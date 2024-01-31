from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=False, required=True)
    password= serializers.CharField(write_only=True, style={'input_type':'password'})
    email = serializers.EmailField(allow_blank=False, required=True)
    first_name = serializers.CharField(allow_blank=False, required=True, max_length=20)
    last_name = serializers.CharField(allow_blank=False, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate_username(self, username):
        # Custom validation for username, you can add your own logic
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError("Username already exists")
        return username
    
    def validate_first_name(self,first_name):
        if User.objects.filter(first_name=  first_name).exists():
            raise serializers.ValidationError('first name already taken')
        return first_name
    
    def validate_last_name(self,last_name):
        if User.objects.filter(last_name = last_name).exists():
            raise serializers.ValidationError("last Name is already taken")
        return last_name
    
    def validate_email(self,email):
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError("email is already taken")
        return email


from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Tutor

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_student', 'is_tutor']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_student', 'is_tutor']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_student=validated_data.get('is_student', False),
            is_tutor=validated_data.get('is_tutor', False)
        )
        return user

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['user']

class TutorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tutor
        fields = ['user', 'subjects_offered', 'bio', 'rating']

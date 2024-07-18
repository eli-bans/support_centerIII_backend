from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Student, Tutor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_student', 'is_tutor']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'is_student', 'is_tutor']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_student=validated_data.get('is_student', False),
            is_tutor=validated_data.get('is_tutor', False)
        )
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['is_student'] = user.is_student
        token['is_tutor'] = user.is_tutor
        return token

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

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        try:
            user = User.objects.get(reset_password_token=value)
            if user.reset_password_token_expires < timezone.now():
                raise serializers.ValidationError("Token has expired.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")
        return value

    def save(self, **kwargs):
        token = self.validated_data['token']
        password = self.validated_data['password']
        user = User.objects.get(reset_password_token=token)
        user.set_password(password)
        user.reset_password_token = None
        user.reset_password_token_expires = None
        user.save()
        return user

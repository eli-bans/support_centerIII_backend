from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Tutor, PasswordReset, User
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
        is_student = validated_data.pop('is_student', False)
        is_tutor = validated_data.pop('is_tutor', False)
        
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_student=is_student,
            is_tutor=is_tutor
        )
        
        if is_student:
            print('Creating student')
            Student.objects.create(user=user)
        
        if is_tutor:
            print('Creating tutor')
            Tutor.objects.create(user=user)
        
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
    user_id = serializers.IntegerField(source='user.id')
    email = serializers.EmailField(source='user.email')
    is_student = serializers.BooleanField(source='user.is_student')
    is_tutor = serializers.BooleanField(source='user.is_tutor')

    class Meta:
        model = Student
        fields = ['id', 'user_id', 'email', 'is_student', 'is_tutor']

class TutorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tutor
        fields = ['user', 'subjects_offered', 'bio', 'rating']


from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        
        return value

    def save(self):
        request = self.context.get('request')
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        # Generate token
        token = default_token_generator.make_token(user)

        # Save token
        PasswordReset.objects.create(email=user.email, token=token, token_expires=timezone.now() + timedelta(minutes=30))

        # Send email
        reset_link = f"{request.scheme}://{request.get_host()}/reset-password/{token}/"
        send_mail(
            'Password Reset Request',
            f'Click the link below to reset your password:\n{reset_link}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        try:
            reset_obj = PasswordReset.objects.get(token=attrs['token'])
            user = User.objects.get(email=reset_obj.email)
        except (TypeError, ValueError, OverflowError, PasswordReset.DoesNotExist):
            raise serializers.ValidationError("Invalid token")
        
        # Set user password
        user.set_password(attrs['new_password'])
        user.save()
        reset_obj.delete()
        return attrs

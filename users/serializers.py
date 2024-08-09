'''
This file contains the serializers for the User, Student, Tutor, PasswordReset models.
It also contains the MyTokenObtainPairSerializer, which is used to customize the JWT token response.
'''
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Student, Tutor, PasswordReset

from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Student, Tutor, PasswordReset, User, Course

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    '''
    Serializer for the User model.
    - id: Integer field to store the user id.
    - email: Email field to store the user email.
    - is_student: Boolean field to indicate if the user is a student.
    - is_tutor: Boolean field to indicate if the user is a tutor.
    '''
    class Meta:
        model = User
        fields = ['id', 'email', 'is_student', 'is_tutor','profile_picture']

class UserRegistrationSerializer(serializers.ModelSerializer):
    '''
    Serializer for user registration.
    '''
    password = serializers.CharField(write_only=True) #password is write only because we don't want to return it in the response
    profile_picture = serializers.ImageField(required=False) #profile picture is not required for registration

    class Meta: 
        '''
        Meta class is used to specify the model and fields for the serializer.
        '''
        model = User
        fields = ['id', 'email', 'password', 'is_student', 'is_tutor','profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        is_student = validated_data.pop('is_student', False) #pop the is_student field from the validated data because it's not part of the User model
        is_tutor = validated_data.pop('is_tutor', False) #pop the is_tutor field from the validated data because it's not part of the User model
        profile_picture = validated_data.pop('profile_picture', None) #pop the profile_picture field from the validated data because it's not part of the User model
        password = validated_data.pop('password') #pop the password field from the validated data because it's not part of the User model
        
        user = User.objects.create_user(   
            email=validated_data['email'],
            is_student=is_student,
            is_tutor=is_tutor,
            profile_picture=profile_picture
        )
        user.set_password(password)
        user.save()

        # if profile_picture:
        #     user.profile_picture = profile_picture
        #     user.save() 
        
        if is_student:
            # print('Creating student')
            Student.objects.create(user=user)
        
        if is_tutor:  # a bit skeptical about this part
            # print('Creating tutor')
            Tutor.objects.create(user=user)
        
        return user

    
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Tutor

class TutorUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    courses = serializers.ListField(child=serializers.ChoiceField(choices=Course.choices))

    class Meta:
        model = Tutor
        fields = ['profile_picture', 'first_name', 'last_name', 'year', 'email', 'courses', 'bio', 'calendly_link']

    def update(self, instance, validated_data):
        courses = validated_data.pop('courses', None)
        instance = super().update(instance, validated_data)
        if courses is not None:
            instance.set_courses(courses)
            instance.save()
        return instance

class TutorCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    courses = serializers.ListField(child=serializers.ChoiceField(choices=Course.choices))
    
    class Meta:
        model = Tutor
        fields = ['email', 'first_name', 'last_name', 'year', 'courses', 'bio', 'calendly_link']

    def create(self, validated_data):
        courses = validated_data.pop('courses', [])
        email = validated_data.pop('email')
        user = User.objects.get(email=email)
        instance = Tutor.objects.create(user=user, **validated_data)
        instance.set_courses(courses)
        instance.save()
        return instance

class StudentSerializer(serializers.ModelSerializer):
    '''
    Provides a way to serialize and deserialize the Student model.
    '''
    user_id = serializers.IntegerField(source='user.id')
    email = serializers.EmailField(source='user.email')
    is_student = serializers.BooleanField(source='user.is_student')
    is_tutor = serializers.BooleanField(source='user.is_tutor')

    class Meta:
        model = Student
        fields = ['id', 'user_id', 'email', 'is_student', 'is_tutor']

class TutorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    profile_picture = serializers.ImageField(required=False)
    courses = serializers.ListField(child=serializers.ChoiceField(choices=Course.choices))

    class Meta:
        model = Tutor
        fields = ['id', 'user', 'profile_picture', 'first_name', 'last_name', 'year', 'courses', 'bio', 'rating', 'calendly_link']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['courses'] = instance.get_courses()
        return ret

    def create(self, validated_data):
        courses = validated_data.pop('courses', [])
        instance = super().create(validated_data)
        instance.set_courses(courses)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        courses = validated_data.pop('courses', None)
        instance = super().update(instance, validated_data)
        if courses is not None:
            instance.set_courses(courses)
            instance.save()
        return instance

class TutorRatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

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

class TutorUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    courses = serializers.ListField(child=serializers.ChoiceField(choices=Course.choices))

    class Meta:
        model = Tutor
        fields = ['profile_picture', 'first_name', 'last_name', 'year', 'email', 'courses', 'bio', 'calendly_link']

    def update(self, instance, validated_data):
        courses = validated_data.pop('courses', None)
        instance = super().update(instance, validated_data)
        if courses is not None:
            instance.set_courses(courses)
            instance.save()
        return instance

class TutorCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    courses = serializers.ListField(child=serializers.ChoiceField(choices=Course.choices))
    
    class Meta:
        model = Tutor
        fields = ['email', 'first_name', 'last_name', 'year', 'courses', 'bio', 'calendly_link']

    def create(self, validated_data):
        courses = validated_data.pop('courses', [])
        email = validated_data.pop('email')
        user = User.objects.get(email=email)
        instance = Tutor.objects.create(user=user, **validated_data)
        instance.set_courses(courses)
        instance.save()
        return instance


class TutorCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    courses = serializers.MultipleChoiceField(choices=Course.choices)
    
    class Meta:
        model = Tutor
        fields = ['email', 'first_name', 'last_name', 'year', 'courses', 'bio', 'calendly_link']

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        user = self.user
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'is_student': user.is_student,
            'is_tutor': user.is_tutor,
        }
        
        if user.is_tutor:
            try:
                tutor = Tutor.objects.get(user=user)
                data['user']['tutor'] = {
                    'first_name': tutor.first_name,
                    'last_name': tutor.last_name,
                    'year': tutor.year,
                    'courses': tutor.get_courses(),
                    'bio': tutor.bio,
                    'rating': tutor.rating,
                    'calendly_link': tutor.calendly_link
                }
            except Tutor.DoesNotExist:
                pass
        
        return data
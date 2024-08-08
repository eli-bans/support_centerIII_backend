'''
This is the models.py file for the users app. 
It contains the models for the User, Student, Tutor, and PasswordReset classes.
'''

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    '''
    Custom user manager for the User model.
    Uses email as the unique identifier for authentication and 
    saves the user with the given email and password.
    '''
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

def profile_picture_upload_path(instance, filename):
    return f'profile_pictures/{instance.id}/{filename}'

class User(AbstractBaseUser, PermissionsMixin):
    '''
    Custom user model with email as the unique identifier.
    - is_student: Boolean field to indicate if the user is a student.
    - is_tutor: Boolean field to indicate if the user is a tutor.
    - reset_password_token: UUID field to store the reset password token.
    - reset_password_token_expires: DateTime field to store the expiration time of the reset password token.
    '''
    email = models.EmailField(unique=True)  # Use email as the unique identifier
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    reset_password_token = models.UUIDField(default=None, null=True, blank=True)
    reset_password_token_expires = models.DateTimeField(default=None, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=profile_picture_upload_path, blank=True, null=True)



    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Student(models.Model):
    '''
    Model for student users.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for students

class Course(models.TextChoices):
    INTRO_TO_AI = 'AI', 'Intro to AI'
    DATA_STRUCTURES = 'DS', 'Data Structure and Algorithms'
    WEB_TECH = 'WT', 'Web Technologies'
    MODELLING = 'MS', 'Modelling and Simulations'

class Tutor(models.Model):
    '''
    Model for tutor users.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    year = models.IntegerField()
    courses = models.CharField(max_length=2, choices=Course.choices, default=Course.INTRO_TO_AI)
    bio = models.TextField(blank=True)
    rating = models.FloatField(default=0.0)
    total_ratings = models.IntegerField(default=0)
    

class PasswordReset(models.Model):
    '''
    Model to store the password reset token and its expiration time.
    '''
    email = models.EmailField()
    token = models.CharField(max_length=100, unique=True, blank=True)
    token_expires = models.DateTimeField(blank=True)

    @classmethod
    def delete_expired_tokens(cls): #delete from db after token expires
        cls.objects.filter(token_expires__lte=timezone.now()).delete()
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
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

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Use email as the unique identifier
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    reset_password_token = models.UUIDField(default=None, null=True, blank=True)
    reset_password_token_expires = models.DateTimeField(default=None, null=True, blank=True)


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for students

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for tutors

class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100, unique=True, blank=True)
    token_expires = models.DateTimeField(blank=True)

    @classmethod
    def delete_expired_tokens(cls):
        cls.objects.filter(token_expires__lte=timezone.now()).delete()
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)

    # Add custom related names to avoid clashes
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

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for students

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for tutors

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import Student, Tutor
from .serializers import UserSerializer, UserRegistrationSerializer, StudentSerializer, TutorSerializer, MyTokenObtainPairSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, TutorRatingSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser


User = get_user_model()

class UserViewSet(generics.ListCreateAPIView):
    '''
    View for listing and creating users.
    '''
    queryset = User.objects.all()
    # parser_classes = (MultiPartParser, FormParser) 

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegistrationSerializer
        return UserSerializer
class AdminUserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_staff = True
        user.is_superuser = True
        user.save()

class MyTokenObtainPairView(TokenObtainPairView):
    '''
    View for obtaining a token pair.
    '''
    serializer_class = MyTokenObtainPairSerializer
    
class UserDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    '''
    View for retrieving, updating, and deleting users.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentViewSet(generics.ListCreateAPIView):
    '''
    View for listing and creating students.
    '''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    

class StudentDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    '''
    View for retrieving, updating, and deleting students.
    '''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TutorViewSet(generics.ListCreateAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            user = serializer.validated_data['user']
            user.is_student = False
            user.is_tutor = True
            user.save()
        else:
            user = self.request.user
            serializer.save(user=user)

    def get_serializer_class(self):
        if self.request.method == 'POST' and self.request.user.is_staff:
            return TutorSerializer
        return TutorSerializer

class TutorDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    '''
    View for retrieving, updating, and deleting tutors.
    '''
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

class TutorRatingView(generics.UpdateAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorRatingSerializer

    def update(self, request, *args, **kwargs):
        tutor = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_rating = serializer.validated_data['rating']
        tutor.total_ratings += 1
        tutor.rating = ((tutor.rating * (tutor.total_ratings - 1)) + new_rating) / tutor.total_ratings
        tutor.save()

        return Response({'rating': tutor.rating}, status=status.HTTP_200_OK)
    

class TutorAverageRatingView(generics.RetrieveAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

    def retrieve(self, request, *args, **kwargs):
        tutor = self.get_object()
        return Response({'average_rating': tutor.rating}, status=status.HTTP_200_OK)

class PasswordResetView(generics.GenericAPIView):
    '''
    View for sending the password reset e-mail.
    '''
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset e-mail has been sent."}, status=200)

class PasswordResetConfirmView(generics.GenericAPIView):
    '''
    View for resetting the password
    '''
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "Password has been reset successfully."}, status=200)

from rest_framework.generics import UpdateAPIView
from .serializers import TutorUpdateSerializer
from .models import Tutor
from rest_framework.permissions import IsAuthenticated

class TutorUpdateView(UpdateAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.get(user=self.request.user)
    
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from .serializers import TutorCreateSerializer
from .models import Tutor

# class TutorCreateView(CreateAPIView):
#     queryset = Tutor.objects.all()
#     serializer_class = TutorCreateSerializer
#     permission_classes = [IsAdminUser]

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
class TutorCreateView(CreateAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorCreateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        email = serializer.validated_data.pop('email')
        user = User.objects.get(email=email)
        
        if user.is_tutor:
            raise ValidationError("This user is already a tutor.")
        
        user.is_student = False
        user.is_tutor = True
        user.save()
        
        serializer.save(user=user)
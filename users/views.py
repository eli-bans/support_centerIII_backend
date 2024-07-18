from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserRegistrationSerializer, StudentSerializer, TutorSerializer
from .models import Student, Tutor


User = get_user_model()

class UserViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegistrationSerializer
        return UserSerializer


from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class UserDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentViewSet(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TutorViewSet(generics.ListCreateAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

class TutorDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer


from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import ForgotPasswordSerializer

class ForgotPasswordView(APIView):
    # permission_classes = []

    # def post(self, request, *args, **kwargs):
    #     serializer = ForgotPasswordSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     email = serializer.validated_data['email']
    #     user = get_object_or_404(User, email=email)
    #     user.generate_reset_token()

    #     reset_link = f'{request.build_absolute_uri("/reset-password/")}{user.reset_password_token}/'
    #     send_mail(
    #         'Password Reset Request',
    #         f'Click the link to reset your password: {reset_link}',
    #         settings.DEFAULT_FROM_EMAIL,
    #         [user.email],
    #     )

        
    #     return Response({'detail': 'Password reset email sent.'}, status=status.HTTP_200_OK)

    def test_email():
        send_mail(
            'Test Email Subject',
            'This is a test email body.',
            settings.DEFAULT_FROM_EMAIL,
            ['palal.asare@ashesi.edu.gh'],  # Replace with a valid email address
        )

    test_email()

class ResetPasswordView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password has been reset.'}, status=status.HTTP_200_OK)

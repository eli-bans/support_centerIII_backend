from rest_framework import generics
from .models import Student, Tutor
from .serializers import UserSerializer, UserRegistrationSerializer, StudentSerializer, TutorSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegistrationSerializer
        return UserSerializer

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

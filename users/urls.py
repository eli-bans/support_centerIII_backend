from django.urls import path
from .views import (UserViewSet, UserDetailViewSet, StudentViewSet, 
                    StudentDetailViewSet, TutorViewSet, TutorDetailViewSet, 
                    MyTokenObtainPairView)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/', UserViewSet.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailViewSet.as_view(), name='user-detail'),
    path('students/', StudentViewSet.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailViewSet.as_view(), name='student-detail'),
    path('tutors/', TutorViewSet.as_view(), name='tutor-list'),
    path('tutors/<int:pk>/', TutorDetailViewSet.as_view(), name='tutor-detail'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
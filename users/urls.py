from django.urls import path
from .views import (UserViewSet, UserDetailViewSet, StudentViewSet, 
                    StudentDetailViewSet, TutorViewSet, TutorDetailViewSet, 
                    MyTokenObtainPairView, PasswordResetView,PasswordResetConfirmView, TutorRatingView, TutorAverageRatingView,AdminUserCreateView, TutorUpdateView,
                     TutorCreateView)
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('users/', UserViewSet.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailViewSet.as_view(), name='user-detail'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('students/', StudentViewSet.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailViewSet.as_view(), name='student-detail'),
    path('tutors/', TutorViewSet.as_view(), name='tutor-list'),
    path('tutors/<int:pk>/', TutorDetailViewSet.as_view(), name='tutor-detail'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tutors/<int:pk>/rate/', TutorRatingView.as_view(), name='tutor-rate'),
    path('tutors/<int:pk>/average-rating/', TutorAverageRatingView.as_view(), name='tutor-average-rating'),
    path('admin-user/', AdminUserCreateView.as_view(), name='admin-user-create'), #this be how we go create admin users
    path('tutors/update/', TutorUpdateView.as_view(), name='tutor-update'),
    path('tutors/create/', TutorCreateView.as_view(), name='tutor-create'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
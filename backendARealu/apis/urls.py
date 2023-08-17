from django.urls import path
from .views import *

urlpatterns = [
    path('send-otp/', SendOtpView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),

    
    path('questions/', QuestionList.as_view(), name='question-list'),
    path('user-response/', UserResponseView.as_view(), name='user-response'),
]


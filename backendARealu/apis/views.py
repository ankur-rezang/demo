from django.conf import settings
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from twilio.rest import Client
from .models import *
import random


# Phone number and otp view


stored_otp_dict = {}


class SendOtpView(APIView):
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = str(random.randint(1000, 9999))

            print(otp)

            stored_otp_dict[phone_number] = otp
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Your OTP is: {otp}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpView(APIView):
    def post(self, request):
        entered_otp = request.data.get('otp')
        phone_number = request.data.get('phone_number')
        stored_otp = stored_otp_dict.get(phone_number)
        if stored_otp and entered_otp == stored_otp:
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


# Questionaire view


class QuestionList(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        question_text = data['question']
        options = data.get('options', [])

        question = Question.objects.create(text=question_text)
        for option_id, option_text in enumerate(options, start=1):
            Option.objects.create(question=question, text=option_text, option_id=option_id)
        
        return Response(status=status.HTTP_201_CREATED)

class UserResponseView(APIView):
    def post(self, request):
        serializer = UserResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

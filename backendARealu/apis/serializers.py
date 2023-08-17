from rest_framework import serializers
from .models import *


# phone number and otp serializers


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class OtpVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField()


# Questionaires serializers


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('text',)

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('text', 'options')

class UserResponseSerializer(serializers.ModelSerializer):
    question_text = serializers.SerializerMethodField()
    selected_option_text = serializers.SerializerMethodField()

    def get_question_text(self, obj):
        return obj.question.text

    def get_selected_option_text(self, obj):
        return obj.selected_option.text

    class Meta:
        model = UserResponse
        fields = ('question_text', 'selected_option_text', 'user_response')

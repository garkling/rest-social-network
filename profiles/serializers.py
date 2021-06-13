from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Profile
from .form_styles import *


class ProfileSerializer(serializers.ModelSerializer):

    last_login = serializers.ReadOnlyField()
    email = serializers.EmailField(style=input_form_style, required=True, label='Email')
    username = serializers.CharField(style=input_form_style, required=True)
    first_name = serializers.CharField(style=input_form_style)
    last_name = serializers.CharField(style=input_form_style)
    bio = serializers.CharField(style=textarea_form_style)

    class Meta:
        model = Profile
        fields = ('email', 'username', 'first_name', 'last_name', 'bio', 'last_login')


class ProfileCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')

        profile = Profile.objects.create_user(username, email, password, **validated_data)
        profile.save()

        return profile


class PasswordUpdateSerializer(serializers.Serializer):

    actual_password = serializers.CharField(required=True, label='Old password')
    new_password1 = serializers.CharField(required=True, label='New password')
    new_password2 = serializers.CharField(required=True, label='Repeat password')

    def validate_actual_password(self, password):
        user = self.context['request'].user
        print('validate old password', user)
        if not user.check_password(password):
            raise serializers.ValidationError('Your old password was entered incorrectly')

        return password

    def validate(self, attrs):
        password1 = attrs.get('new_password1')
        password2 = attrs.get('new_password2')
        print('validate', password1, password2)
        if not (password1 or password2) or password1 != password2:
            raise serializers.ValidationError(
                {'new_password2': "The passwords didn't match."}
            )

        validate_password(password1, self.context['request'].user)
        return attrs

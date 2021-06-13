from rest_framework import serializers

from .models import Post, PostRating
from .form_styles import *


class PostSerializer(serializers.ModelSerializer):

    title = serializers.CharField(style=input_form_style, required=True, label='')
    content = serializers.CharField(style=textarea_form_style, required=True, label='')
    author = serializers.CharField(source='get_author', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author']
        read_only_fields = ['id']


class PostRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostRating
        fields = '__all__'

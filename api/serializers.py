from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    def validate(self, data):
        user = self.context['request'].user
        if data['following'] == user:
            raise serializers.ValidationError(
                'You cannot subscribe to yourself')
        return data

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'following'],
            message='You already subscribe this user.')
        ]

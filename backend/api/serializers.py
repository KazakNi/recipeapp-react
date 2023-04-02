from djoser.serializers import UserCreateSerializer
from users.models import MyUser, Subscription
from recipes.models import Tag
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(UserCreateSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password', 'is_subscribed',)

    def get_is_subscribed(self, obj):

        user = self.context['request'].user
        if user.is_anonymous or (user == obj):
            return False
        return user.follower.filter(author=obj).exists()

    def create(self, validated_data: dict) -> User:

        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)

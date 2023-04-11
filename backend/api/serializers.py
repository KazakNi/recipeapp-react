from djoser.serializers import UserCreateSerializer
from users.models import MyUser
from recipes.models import Tag, Recipe, Ingredient, Favorites, RecipeIngredients, Basket
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ReadOnlyField
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


class RecipesSubscriber(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class UserSubscribersSerializer(UserSerializer):
    recipes = SerializerMethodField(read_only=True)
    recipes_count = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        limit = int(self.context['recipes_limit'])
        recipes = Recipe.objects.filter(author=obj)[:limit]
        serializer = RecipesSubscriber(instance=recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_is_subscribed(self, obj):
        return True


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class IngrediendAmountSerializer(ModelSerializer):
    name = ReadOnlyField(source='ingredients.name')
    measurement_unit = ReadOnlyField(source='ingredients.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(ModelSerializer):
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngrediendAmountSerializer(many=True, required=False,
                                             source='recipe')
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if self.context['is_favorited']:
            return True
        else:
            return obj.favorite_recipes.filter(author=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if self.context['is_in_shopping_cart']:
            return True
        else:
            return obj.in_cart.filter(author=user).exists()

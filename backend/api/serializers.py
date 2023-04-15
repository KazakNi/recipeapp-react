from djoser.serializers import UserCreateSerializer
from users.models import MyUser
from recipes.models import Tag, Recipe, Ingredient, RecipeIngredients
from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        ReadOnlyField, PrimaryKeyRelatedField,
                                        IntegerField)
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField

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


class RecipeBaseSerializer(ModelSerializer):
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart')


class RecipeReadSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(RecipeBaseSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngrediendAmountSerializer(many=True, required=True,
                                             source='recipe')

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients',
                  'tags', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if self.context['is_favorited']:
                return True
            else:
                return obj.favorite_recipes.filter(author=user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if self.context['is_in_shopping_cart']:
                return True
            else:
                return obj.in_cart.filter(author=user).exists()
        return False


class IngredientCreateSerializer(ModelSerializer):
    name = ReadOnlyField(source='ingredients.name')
    measurement_unit = ReadOnlyField(
        source='ingredients.measurement_unit')
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount', 'name', 'measurement_unit')


class RecipeCreateSerializer(RecipeBaseSerializer):
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = IngredientCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients',
                  'tags', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

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

    def create_ingredients(self, ingredients, recipe):
        res = []
        for ingredient in ingredients:
            res.append(RecipeIngredients(
                recipe=recipe,
                ingredients=ingredient['id'],
                amount=ingredient['amount']
            ))

        RecipeIngredients.objects.bulk_create(res)

    def create(self, validated_data):
        user = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.get('ingredients', instance.ingredients)
        tags = validated_data.get('tags', instance.tags)
        if tags:
            instance.tags.clear()
            instance.tags.set(tags)

        if ingredients:
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)

        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data

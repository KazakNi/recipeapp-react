from django.db import models
from django.utils.text import slugify
from users.models import MyUser
from django.core.validators import MinValueValidator


class Tag(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify('tag' + '-' + self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):

    name = models.CharField(max_length=130)
    measurement_unit = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                               related_name='recipes')
    name = models.CharField(max_length=200, verbose_name='݀Название')
    image = models.ImageField(upload_to='recipes/images/')
    text = models.TextField(max_length=300, verbose_name='Описание')
    ingredients = models.ManyToManyField(to=Ingredient, related_name='recipes',
                                         through_fields=('recipe', 
                                                         'ingredients'),
                                         through='RecipeIngredients')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в мин.',
        validators=[MinValueValidator(1, 'Время приготовления не может'
                                      'быть меньше минуты!')])

    def __str__(self) -> str:
        return self.name


class RecipeIngredients(models.Model):

    ingredients = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, 'Кол-во ингредиента не может'
                                      'быть меньше единицы.')])
    
    def __str__(self) -> str:
        return self.recipe.name


class Favorites(models.Model):

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                               related_name='favorites')
    recipes = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                                related_name='favorites')


class Basket(models.Model):

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                               related_name='in_cart')
    recipes = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                                related_name='in_cart')

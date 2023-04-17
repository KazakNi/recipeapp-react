from django.db import models
from django.utils.text import slugify
from users.models import MyUser
from django.core.validators import MinValueValidator


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name='Название')
    color = models.CharField(max_length=7, unique=True, verbose_name='Цвет')
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):

    name = models.CharField(max_length=130, blank=False, null=False,
                            verbose_name='Наименование')
    measurement_unit = models.CharField(max_length=15, blank=False, null=False,
                                        verbose_name='Ед. изм.')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='ܻАвтор')
    name = models.CharField(max_length=200, verbose_name='݀Название')
    image = models.ImageField(upload_to='recipes/images/')
    text = models.TextField(max_length=300, verbose_name='Описание')
    ingredients = models.ManyToManyField(to=Ingredient, related_name='recipes',
                                         through_fields=('recipe',
                                                         'ingredients'),
                                         through='RecipeIngredients',
                                         blank=False)
    tags = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в мин.',
        validators=[MinValueValidator(1, 'Время приготовления не может'
                                      'быть меньше минуты!')])
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredients(models.Model):

    ingredients = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE, related_name='ingredient')
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe')
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, 'Кол-во ингредиента не может'
                                      'быть меньше единицы.')], 
        blank=False,
        null=False)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredients'),
                name='unique ingredient')]

    def __str__(self) -> str:
        return self.recipe.name


class Favorites(models.Model):

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                               related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorite_recipes')

    class Meta:
        unique_together = [['author', 'recipe']]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
    
    def __str__(self) -> str:
        return f'Рецепт {self.recipe} в избранном {self.author}'


class Basket(models.Model):

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                               related_name='in_cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='in_cart')

    class Meta:
        unique_together = [['author', 'recipe']]
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self) -> str:
        return f'Рецепт {self.recipe} в корзине пользователя {self.author}'
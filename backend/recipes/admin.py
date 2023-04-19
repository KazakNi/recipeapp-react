from django.contrib import admin
from .models import (Tag, Recipe, RecipeIngredients,
                     Ingredient, Favorites, Basket)
from django.utils.safestring import mark_safe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    prepopulated_fields = {'slug': ('name',), }


class RecipeInline(admin.TabularInline):
    model = RecipeIngredients


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        RecipeInline,
    ]
    exclude = ('ingredients',)
    list_display = ('name', 'author', 'show_favorites')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('show_favorites', 'image_tag')

    def image_tag(self, obj):
        print(obj.image.url)
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    image_tag.short_description = 'Image'

    def show_favorites(self, obj):
        result = obj.favorite_recipes.all().count()
        return result
    show_favorites.short_description = 'В избранном'


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class Ingredient(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name', 'measurement_unit')


@admin.register(Favorites)
class Favorite(admin.ModelAdmin):
    pass


@admin.register(Basket)
class Cart(admin.ModelAdmin):
    pass

from django.contrib import admin
from .models import Tag, Recipe, RecipeIngredients, Ingredient

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class RecipeInline(admin.TabularInline):
    model = RecipeIngredients

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        RecipeInline,
    ]
    exclude = ('ingredients',)


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    pass

@admin.register(Ingredient)
class Ingredient(admin.ModelAdmin):
    pass
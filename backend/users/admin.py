from django.contrib import admin
from .models import MyUser, Subscriptions


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('email', 'first_name')


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    pass

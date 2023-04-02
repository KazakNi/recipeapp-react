from django.contrib import admin
from .models import MyUser, Subscription

@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('email', 'first_name')
    

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


